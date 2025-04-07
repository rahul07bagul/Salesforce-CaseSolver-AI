import { LightningElement, api, wire, track } from 'lwc';
import { getRecord, getFieldValue } from 'lightning/uiRecordApi';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import Python_App_URL from '@salesforce/label/c.Python_App_URL';

import SUBJECT_FIELD from '@salesforce/schema/Case.Subject';
import DESCRIPTION_FIELD from '@salesforce/schema/Case.Description'; 

export default class CaseResolutionDisplay extends LightningElement {
    @api recordId; 
    @api endpointUrl = Python_App_URL;

    @track htmlResult;
    @track error;
    @track isLoading = false;

    @wire(getRecord, { recordId: '$recordId', fields: [SUBJECT_FIELD, DESCRIPTION_FIELD] })
    caseRecord;

    get subject() {
        return this.caseRecord.data ? getFieldValue(this.caseRecord.data, SUBJECT_FIELD) : 'Test';
    }

    get description() {
        return getFieldValue(this.caseRecord.data, DESCRIPTION_FIELD) || '';
    }

    async handleGetResolutionClick() {
        if (!this.subject || !this.recordId) {
            this.showToast('Error', 'Case data not loaded yet.', 'error');
            return;
        }
        if (!this.endpointUrl) {
             this.showToast('Configuration Error', 'API Endpoint URL is not configured.', 'error');
             this.error = 'API Endpoint URL is not configured for this component.';
             return;
        }

        this.isLoading = true;
        this.error = null; // Clear previous errors
        this.htmlResult = null; // Clear previous results

        const payload = {
            case_id: this.recordId,
            subject: this.subject,
            body: this.description
        };

        try {
            const response = await fetch(this.endpointUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const responseBodyText = await response.text();

            if (response.ok) {
                this.htmlResult = responseBodyText;
                this.showToast('Success', 'Resolution suggestion received.', 'success');
            } else {
                console.error('API Error Response:', response.status, responseBodyText);
                const errorMatch = responseBodyText.match(/<div class="error">.*?<pre>(.*?)<\/pre>.*?<\/div>/is);
                const displayError = errorMatch ? errorMatch[1].trim() : `Server responded with status ${response.status}. Check console for details.`;
                this.error = `Failed to get resolution: ${displayError}`;
                this.showToast('API Error', this.error, 'error');
            }
        } catch (error) {
            console.error('Fetch Error:', error);
            this.error = `Network error or CORS issue: ${error.message}. Make sure the API is running, CORS is configured, and Remote Site Setting exists.`;
            this.showToast('Error', 'Could not connect to the resolution service.', 'error');
        } finally {
            this.isLoading = false;
        }
    }

    renderedCallback() {
        const container = this.template.querySelector('.resolution-container');
        if (container && this.htmlResult) {
            this.renderResolution();
        } else if (container) {
             container.innerHTML = '';
        }
    }

    showToast(title, message, variant) {
        const event = new ShowToastEvent({
            title: title,
            message: message,
            variant: variant,
        });
        this.dispatchEvent(event);
    }

    renderResolution() {
        if (this.htmlResult) {
            const container = this.template.querySelector('.resolution-container');
            
            if (container) {
                try {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(this.htmlResult, 'text/html');
                    
                    const successDiv = doc.querySelector('.success pre');
                    
                    if (successDiv) {
                        const escapedHtml = successDiv.textContent;
                        
                        const decodedHtml = this.decodeHtmlEntities(escapedHtml);
                        
                        const wrapperDiv = document.createElement('div');
                        wrapperDiv.className = 'success-content';
                        wrapperDiv.innerHTML = decodedHtml;
                        
                        container.innerHTML = '';
                        container.appendChild(wrapperDiv);
                    } else {
                        container.innerHTML = this.htmlResult;
                    }
                } catch (error) {
                    console.error('Error rendering resolution:', error);
                    container.innerHTML = this.htmlResult;
                }
            }
        }
    }

    decodeHtmlEntities(encodedString) {
        const textarea = document.createElement('textarea');
        textarea.innerHTML = encodedString;
        return textarea.value;
    }
}