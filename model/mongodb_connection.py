from pymongo import MongoClient

client = None

def connect_to_mongodb():
    global client
    if client is None:
        try:
            client = MongoClient("mongodb://localhost:27017/")
        except Exception as e:
            print(f"Lỗi khi kết nối MongoDB: {e}")
            return None
    return client['ha_DB']
