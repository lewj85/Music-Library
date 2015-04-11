from implementation.primaries.ExtractMetadata.classes import MetaParser

class OnlineMetaParser(MetaParser.MetaParser):
    '''
    class which applies same meta parsing rules to files which have been temporarily downloaded from an api.
    will ignore a select set of tags specified by the instantiator
    '''
    def __init__(self, ignored=[], source=""):
        MetaParser.MetaParser.__init__(self)
        self.ignored = ignored
        [self.handlers.pop(i) for i in self.ignored]
        self.source = source

    def CollatePartsIntoData(self):
        MetaParser.MetaParser.CollatePartsIntoData(self)
        self.data["source"] = self.source
