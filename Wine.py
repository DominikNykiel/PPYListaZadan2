class Wine:
    def __init__(self, decisiveAttribute, listOfOtherAttributes):
        self.attribute = decisiveAttribute
        self.listOfAttributes = listOfOtherAttributes

    def __repr__(self):
        return f"Wine(decisiveAttribute={self.attribute},listOfOtherAttributes = {self.listOfAttributes})"
