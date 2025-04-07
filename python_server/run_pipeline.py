from services.service import Service

service = Service()
service.run_data_pipeline("data\purdue_kb_vector.json", "json")