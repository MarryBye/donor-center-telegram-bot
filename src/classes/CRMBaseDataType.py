class CRMBaseDataType:
    def __init__(self, data: dict=None):
        self.data = {
            "ID": None
        }
            
        if data is not None:
            self.form(data)
        
    def form(self, data: dict):
        for data_component in data:
            self.data[data_component] = data[data_component]
            
        return self
    
    def get_data(self) -> tuple:
        return self.data.values()
    
    def set_id(self, id: int):
        self.data["ID"] = id
        
    def get_id(self) -> int:
        return self.data["ID"]