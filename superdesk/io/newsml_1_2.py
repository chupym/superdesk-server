
import datetime
from ..etree import etree


class Parser():
    """NewsMl xml 1.2 parser"""
    
    subject_code_to_name = sorted([
        ('01', 'art/culture'),
        ('02', 'crime law and justice'),
        ('03', 'disasters and accidents'),
        ('04', 'economic news'),
        ('05', 'education'),
        ('06', 'environmental issues'),
        ('07', 'health'),
        ('08', 'human interest'),
        ('08999', 'general'),
        ('09', 'labour'),
        ('10', 'lifestyle and leisure - then trade unions'),
        ('11', 'politics'),
        ('11998', 'mag'),
        ('11999', 'int'),
        ('12', 'religion'),
        ('13', 'science'),
        ('14', 'social issues'),
        ('15', 'sport'),
        ('1503', 'horse races – french wire only')
    ], key=lambda entry: entry[0], reverse=True)

    def parse_message(self, tree):
        """Parse NewsMessage."""
        item = {}
        self.root = tree

        item['NewsIdentifier'] = self.parse_elements(tree.find('NewsItem/Identification/NewsIdentifier'))
        item['NewsManagement'] = self.parse_elements(tree.find('NewsItem/NewsManagement'))
        item['NewsLines'] = self.parse_elements(tree.find('NewsItem/NewsComponent/NewsLines'))
        item['Provider'] = self.parse_attributes_as_dictionary(
            tree.find('NewsItem/NewsComponent/AdministrativeMetadata/Provider'))
        item['DescriptiveMetadata'] = self.parse_multivalued_elements(
            tree.find('NewsItem/NewsComponent/DescriptiveMetadata'))
        item['located'] = self.process_located(self.parse_attributes_as_dictionary(
            tree.find('NewsItem/NewsComponent/DescriptiveMetadata/Location')))

        keywords = tree.findall('NewsItem/NewsComponent/DescriptiveMetadata/Property')
        item['keywords'] = self.parse_attribute_values(keywords, 'Keyword')

        subjects = tree.findall('NewsItem/NewsComponent/DescriptiveMetadata/SubjectCode/SubjectDetail')
        subjects += tree.findall('NewsItem/NewsComponent/DescriptiveMetadata/SubjectCode/SubjectMatter')
        subjects += tree.findall('NewsItem/NewsComponent/DescriptiveMetadata/SubjectCode/Subject')

        item['Subjects'] = self.parse_attributes_as_dictionary(subjects)
        item['ContentItem'] = self.parse_attributes_as_dictionary(
            tree.find('NewsItem/NewsComponent/ContentItem'))
        # item['Content'] = etree.tostring(
        #       tree.find('NewsItem/NewsComponent/ContentItem/DataContent/nitf/body/body.content'))
        item['body_html'] = etree.tostring(
            tree.find('NewsItem/NewsComponent/ContentItem/DataContent/nitf/body/body.content'))

        return self.populate_fields(item)

    def parse_elements(self, tree):
        items = {}
        for item in tree:
            if item.text is None:
                # read the attribute for the item
                if item.tag != 'HeadLine':
                    items[item.tag] = item.attrib
            else:
                # read the value for the item
                items[item.tag] = item.text
        return items

    def parse_multivalued_elements(self, tree):
        items = {}
        for item in tree:
            if item.tag not in items:
                items[item.tag] = [item.text]
            else:
                items[item.tag].append(item.text)

        return items

    def parse_attributes_as_dictionary(self, items):
        attributes = [item.attrib for item in items]
        return attributes

    def parse_attribute_values(self, items, attribute):
        attributes = []
        for item in items:
            if item.attrib['FormalName'] == attribute:
                attributes.append(item.attrib['Value'])
        return attributes

    def datetime(self, string):
        return datetime.datetime.strptime(string, '%Y%m%dT%H%M%S+0000')

    def populate_fields(self, item):
        item['guid'] = item['NewsIdentifier']['PublicIdentifier']
        item['provider'] = item['Provider'][0]['FormalName']
        item['type'] = 'text'
        item['urgency'] = item['NewsManagement']['Urgency']['FormalName']
        item['version'] = item['NewsIdentifier']['RevisionId']
        item['versioncreated'] = self.datetime(item['NewsManagement']['ThisRevisionCreated'])
        item['firstcreated'] = self.datetime(item['NewsManagement']['FirstCreated'])
        item['pubstatus'] = item['NewsManagement']['Status']['FormalName']
        item['subject'] = self.process_subject(item['Subjects'])

        if 'HeadLine' in item['NewsLines']:
            item['headline'] = item['NewsLines']['HeadLine']
        elif item['NewsManagement']['NewsItemType']['FormalName'] == 'Alert':
            item['headline'] = 'Alert'

        return item
    
    def process_subject(self, subjects):
        processed = []
        for subject in subjects:
            if not 'FormalName' in subject: continue
            qcode = subject['FormalName']
            item = {'qcode': qcode}
            processed.append(item)
            
            for prefix, name in self.subject_code_to_name:
                if qcode.startswith(prefix):
                    item['name'] = name
                    break
                
        return processed
    
    def process_located(self, locations):
        processed = []
        for located in locations:
            if not 'FormalName' in located: continue
            if located['FormalName'].lower() == 'city':
                processed.append({'name': located['Value'].upper()})
        return processed