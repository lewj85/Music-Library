from implementation.primaries.Drawing.classes import BaseClass

class Meta(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "title" in kwargs:
            if kwargs["title"] is not None:
                self.title = kwargs["title"]
        if "composer" in kwargs:
            if kwargs["composer"] is not None:
                self.composer = kwargs["composer"]

    def toLily(self):
        val = "\header {\n"
        if hasattr(self, "title"):
            val += "title = \""+self.title+"\""
        if hasattr(self, "composer"):
            val += "composer = \""+self.composer +"\""
        val += "\n}"
        return val

