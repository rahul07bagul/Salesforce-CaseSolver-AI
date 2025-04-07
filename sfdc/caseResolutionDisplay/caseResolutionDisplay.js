import { LightningElement, api, wire, track } from 'lwc';
import { getRecord, getFieldValue } from 'lightning/uiRecordApi';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import Python_App_URL from '@salesforce/label/c.Python_App_URL';

import SUBJECT_FIELD from '@salesforce/schema/Case.Subject';
import DESCRIPTION_FIELD from '@salesforce/schema/Case.Description'; 

export default class CaseResolutionDisplay extends LightningElement {
    @api recordId; 
    @api endpointUrl = Python_App_URL;

    @track htmlResult = `<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Case Resolution</title>
    <style>
        body {
            font-family: sans-serif;
            padding: 20px;
        }

        .container {
            border: 1px solid #ccc;
            padding: 15px;
            border-radius: 5px;
        }

        .error {
            color: red;
            border-left: 5px solid red;
            padding-left: 10px;
            background-color: #ffebeb;
        }

        .success {
            color: green;
            border-left: 5px solid green;
            padding-left: 10px;
            background-color: #e6ffed;
        }

        h2 {
            margin-top: 0;
        }

        h3 {
            margin-top: 20px;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }

        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            background-color: #f9f9f9;
            padding: 10px;
            border: 1px solid #eee;
            border-radius: 3px;
        }
    </style>
</head>

<body>

    <div class="container">
        <h2>Case Details</h2>
        <p><strong>Case ID:</strong> 120000</p>
        <p><strong>Subject:</strong> Related to flow trigger</p>
        <p><strong>Body:</strong></p>
        <pre>more information about flow trigger</pre>

        <hr>


        <h2>Suggested Resolution</h2>
        <div class="success">
            <pre>&lt;p&gt;Thank you for contacting Salesforce Support. I understand you&#39;re inquiring about flow triggers.&lt;/p&gt;

&lt;p&gt;Unfortunately, the knowledge base articles provided do not contain specific information about general flow trigger information.&lt;/p&gt;

&lt;p&gt;Based on my understanding, here&#39;s some general information about flow triggers:&lt;/p&gt;

&lt;ul&gt;
    &lt;li&gt;&lt;b&gt;Record-Triggered Flows:&lt;/b&gt; These flows start when a record is created, updated, or deleted. You can configure them to run before or after the record change.&lt;/li&gt;
    &lt;li&gt;&lt;b&gt;Schedule-Triggered Flows:&lt;/b&gt; These flows run at a specified time and frequency, allowing you to automate processes on a recurring schedule.&lt;/li&gt;
    &lt;li&gt;&lt;b&gt;Platform Event-Triggered Flows:&lt;/b&gt; These flows start when a platform event message is received, enabling you to integrate Salesforce with external systems.&lt;/li&gt;
    &lt;li&gt;&lt;b&gt;Autolaunched Flows:&lt;/b&gt; These flows don&#39;t have a trigger and must be started by another process, such as an Apex class, a button click, or another flow.&lt;/li&gt;
&lt;/ul&gt;

&lt;p&gt;When configuring flow triggers, consider the following:&lt;/p&gt;

&lt;ul&gt;
    &lt;li&gt;&lt;b&gt;Entry Conditions:&lt;/b&gt; Define the conditions that must be met for the flow to run. This ensures the flow only runs when necessary.&lt;/li&gt;
    &lt;li&gt;&lt;b&gt;Trigger Timing:&lt;/b&gt; Decide whether the flow should run before or after the record change. Before-save flows can make changes to the record being saved, while after-save flows can perform actions like sending emails or updating related records.&lt;/li&gt;
    &lt;li&gt;&lt;b&gt;Governor Limits:&lt;/b&gt; Be mindful of Salesforce governor limits, especially when dealing with large data volumes or complex logic. Optimize your flow to avoid hitting these limits.&lt;/li&gt;
&lt;/ul&gt;

&lt;p&gt;These details should provide a solid understanding of flow triggers. If you have more specific questions or encounter issues, please submit a new case with detailed information.&lt;/p&gt;
</pre>
        </div>


    </div>

</body>

</html>`;
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