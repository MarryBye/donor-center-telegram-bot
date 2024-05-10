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
    
    def is_data_empty(self) -> bool:
        empty = True
        for data_component in self.data:
            if self.data[data_component] != None:
                empty = False
        return empty
    
    def is_full(self) -> bool:
        full = True
        for data_component in self.data:
            if self.data[data_component] is None:
                full = False
        return full
    
    def get_from_data(self, key_name: str):
        return self.data[key_name] if key_name in self.data else None
    
    def set_id(self, id: int):
        self.data["ID"] = id
        
    def get_id(self) -> int:
        return self.get_from_data(key_name="ID")