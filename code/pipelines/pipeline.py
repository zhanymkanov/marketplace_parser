import json
class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.json', 'w+', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        print("---------------------THERE------------------")
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item