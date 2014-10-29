from superdesk.io.newsml_1_2 import Parser
from superdesk.etree import etree
from unittest.case import TestCase

TEST_XML = '''<?xml version="1.0" encoding="utf-8"?>
<NewsML Version="1.2">
<!--AFP NewsML text-photo profile evolution2-->
<!--Processed by Xafp1-4ToNewsML1-2 rev23-->
<Catalog Href="http://www.afp.com/dtd/AFPCatalog.xml"/>
<NewsEnvelope>
<TransmissionId>0343</TransmissionId>
<DateAndTime>20140821T043324Z</DateAndTime>
<NewsService FormalName="DGTE"/>
<NewsProduct FormalName="PAW"/>
<NewsProduct FormalName="AFW"/>
<NewsProduct FormalName="MEW"/>
<NewsProduct FormalName="EUW"/>
<NewsProduct FormalName="MAX"/>
<NewsProduct FormalName="ANA"/>
<NewsProduct FormalName="DGTE"/>
<NewsProduct FormalName="DVBP"/>
<NewsProduct FormalName="DAGI"/>
<NewsProduct FormalName="DILI"/>
<NewsProduct FormalName="DVBA"/>
<NewsProduct FormalName="DVBF"/>
<Priority FormalName="4"/>
</NewsEnvelope>
<NewsItem xml:lang="en">
<Identification>
<NewsIdentifier>
<ProviderId>afp.com</ProviderId>
<DateId>20140821T043319Z</DateId>
<NewsItemId>TX-PAR-FEE18</NewsItemId>
<RevisionId PreviousRevision="0" Update="N">1</RevisionId>
<PublicIdentifier>urn:newsml:afp.com:20140821T043319Z:TX-PAR-FEE18:1</PublicIdentifier>
</NewsIdentifier>
<NameLabel>Indonesia-election-court</NameLabel>
</Identification>
<NewsManagement>
<NewsItemType FormalName="News"/>
<FirstCreated>20140821T043303+0000</FirstCreated>
<ThisRevisionCreated>20140821T043303+0000</ThisRevisionCreated>
<Status FormalName="Usable"/>
<Urgency FormalName="4"/>
<AssociatedWith NewsItem="urn:newsml:afp.com:20140821:a037e6d1-5d84-46d4-8b1b-a6b477d3b20b"/>
<AssociatedWith FormalName="Photo"/>
</NewsManagement>
<NewsComponent>
<NewsLines>
<DateLine>JAKARTA, Aug 21, 2014 (AFP) -</DateLine>
<HeadLine xml:lang="en">Indonesian court to rule on presidential election challenge</HeadLine>
<NewsLine>
<NewsLineType FormalName="ProductLine"/>
<NewsLineText>(PICTURE)</NewsLineText>
</NewsLine>
</NewsLines>
<AdministrativeMetadata>
<Provider>
<Party FormalName="AFP"/>
</Provider>
<Creator>
<Party FormalName="Presi Mandari "/>
</Creator>
</AdministrativeMetadata>
<DescriptiveMetadata>
<Language FormalName="en"/>
<Genre FormalName="Recit"/>
<SubjectCode>
<SubjectMatter FormalName="11003000" cat="POL"/>
</SubjectCode>
<SubjectCode>
<SubjectMatter FormalName="02007000" cat="CLJ"/>
</SubjectCode>
<SubjectCode>
<Subject FormalName="02000000" cat="CLJ"/>
</SubjectCode>
<SubjectCode>
<Subject FormalName="11000000" cat="POL"/>
</SubjectCode>
<SubjectCode>
<SubjectMatter FormalName="02007000" cat="CLJ"/>
</SubjectCode>
<OfInterestTo FormalName="ASI-TEG-1=PAW"/>
<OfInterestTo FormalName="EAA-TEG-1=AFW"/>
<OfInterestTo FormalName="EAA-TEG-1=MEW"/>
<OfInterestTo FormalName="EAA-TEG-1=EUW"/>
<OfInterestTo FormalName="MAX-TEG-1=MAX"/>
<OfInterestTo FormalName="ANA-TEG-1=ANA"/>
<DateLineDate>20140821T043303+0000</DateLineDate>
<Location HowPresent="Origin">
<Property FormalName="Country" Value="IDN"/>
<Property FormalName="City" Value="Jakarta"/>
</Location>
<Property FormalName="GeneratorSoftware" Value="libg2"/>
<Property FormalName="Keyword" Value="Indonesia"/>
<Property FormalName="Keyword" Value="election"/>
<Property FormalName="Keyword" Value="court"/>
</DescriptiveMetadata>
<ContentItem>
<MediaType FormalName="Text"/>
<Format FormalName="NITF3.1"/>
<Characteristics>
<SizeInBytes>3648</SizeInBytes>
<Property FormalName="Words" Value="608"/>
</Characteristics>
<DataContent>
<nitf>
<body>
<body.content>
<p>An Indonesian court was Thursday expected to uphold Joko Widodo's victory in last month's presidential election, rejecting claims of widespread cheating from his opponent after weeks of political uncertainty in the world's third-biggest democracy.</p>
<p>Ahead of the Constitutional Court ruling, hundreds of supporters of Prabowo Subianto, the ex-general who lost the election, were staging noisy rallies in Jakarta while police and soldiers were out in force around the capital.</p>
<p>"I believe that Prabowo is the true president," said Dalianto, a 57-year-old supporter at a rally in downtown Jakarta who like many Indonesians goes by one name.</p>
<p>"The election commission cheated in their count of the votes."</p>
<p>The court was set to hand down its ruling on Thursday afternoon after two weeks of hearings, with independent analysts expecting the nine-judge panel to reject Prabowo's challenge. The verdict cannot be appealed.</p>
<p>Both Prabowo, a top military figure in the era of dictator Suharto with a chequered human rights record, and Widodo, the reform-minded governor of Jakarta, declared victory at the July 9 election.</p>
<p>However official results released after a two-week count across the vast archipelago showed Widodo won a decisive, six-point victory after the tightest, most polarising election since authoritarian rule ended in 1998.</p>
<p>The 53-year-old, who won legions of fans with his down-to-earth approach as Jakarta governor and is known by his nickname Jokowi, is the country's first leader from outside the political and military elites.</p>
<p>However Prabowo -- who has been seeking the presidency for a decade -- has refused to accept the results and his team filed a lengthy complaint against the election commission with the Constitutional Court, which has the final say on poll disputes.</p>
<p>They say he is the true winner of the election, that fraud occurred at tens of thousands of polling stations, and that election officials failed to order recounts in numerous places where they should have.</p>
<p>However evidence presented by Prabowo's team has not been regarded as convincing.</p>
<p>"They are going to throw out the suit," said Tobias Basuki, a political analyst from Jakarta-based think-tank the Centre for Strategic and International Studies, adding that the evidence was "very weak".</p>
<p> </p>
<hl2>- 'Our struggle has just started' - </hl2>
<p> </p>
<p>Legal challenges were mounted after Indonesia's two previous direct presidential elections, in 2004 and 2009, and both failed. </p>
<p>The huge team of lawyers for Prabowo, now a wealthy businessman, has been left red-faced at times by unconvincing witness testimony. </p>
<p>One witness claimed to be a village girl from the mountains who supported Prabowo -- only for it to emerge later she held a senior position with the ex-general's party in eastern Papua province. </p>
<p>Security was tight for the announcement, with around 4,000 police on duty at the court and roads leading up to the building blocked off.</p>
<p>Supporters have been staging rallies at the court over the past two weeks, although they have been peaceful.</p>
<p>Another 30,000 security personnel, including soldiers and police, will be deployed around the capital. </p>
<p>A spokesman for outgoing President Susilo Bambang Yudhoyono said that the leader hoped the ruling "will be accepted by all the Indonesian people".</p>
<p>Even if he loses, Prabowo has pledged to fight on, telling supporters this week that "our struggle has just started". But analysts believe he has no other realistic options left to challenge the result.</p>
<p>A loss for Prabowo in court would clear the way for Widodo to focus on forming his administration and formulating policy before his October 20 inauguration.</p>
<p>He has already set up a "transition team" to shape policy and pick his cabinet, and asked the public to suggest who they would like to be ministers in an online poll.</p>
<p>prm-sr/jah</p>
</body.content>
</body>
</nitf>
</DataContent>
</ContentItem>
</NewsComponent>
</NewsItem>
</NewsML>
'''

class TestNEWSML(TestCase):

    def test_subject(self):
        item = Parser().parse_message(etree.fromstring(TEST_XML))
        self.assertEqual(item['subject'], [{'name': 'politics', 'qcode': '11003000'}, 
                                           {'name': 'crime law and justice', 'qcode': '02007000'}, 
                                           {'name': 'crime law and justice', 'qcode': '02007000'}, 
                                           {'name': 'crime law and justice', 'qcode': '02000000'}, 
                                           {'name': 'politics', 'qcode': '11000000'}])
        
        self.assertEqual(item['located'], [{'name': 'JAKARTA'}])