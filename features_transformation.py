from nltk.tokenize import SpaceTokenizer
from nltk.tag.stanford import StanfordNERTagger

#NEED TO SET ENV FOR PROJECT LATER

jar = "libs/stanford-ner.jar"
classifier = "libs/english.all.3class.distsim.crf.ser.gz"

ner_tagger = StanfordNERTagger(classifier, jar, encoding='utf8')

#more information https://stanfordnlp.github.io/CoreNLP/
#https://nlp.stanford.edu/software/tagger.shtml#History
#import only English
#st = StanfordNERTagger('stanford-english-corenlp-2016-10-31-models.jar')

raw_test_data = "President Donald Trump may have nothing to hide when it comes to alleged links between his campaign and Russia -- but he is behaving in a way that makes it look like he does.Ex-CIA chief John Brennan: &#39;Russia brazenly interfered&#39; in US elections Ex-CIA chief John Brennan: 'Russia brazenly interfered' in US electionsThe President now facing questions about two potential incidents of obstruction of justice: applying pressure on and eventually firing FBI Director James Comey, and separately leaning on National Security Agency Director Adm. Mike Rogers and Director of National Intelligence Dan Coats to publicly deny any collusion between his aides and a Russian operation to disrupt the election last year, according to sources cited by The Washington Post and CNN.Of all the rapid-fire revelations, these could be the most serious. They indicate not just a single decision, but a possible pattern of behavior -- the scope of which appears to be broadening. A key question moving forward will be whether the President or his advisers had intent to influence the investigation into contacts between Russia and his campaign, or whether Trump's actions were solely an attempt to manage a bad public relations cycle.The eye-opening new chapter in the swirling Russia saga unfolded as Trump was trying to recast the political narrative of a young presidency already facing an existential crisis.Coats not commenting on report Trump asked him to deny evidence of Russia collusionCoats not commenting on report Trump asked him to deny evidence of Russia collusionBut as he basked in red carpet welcomes -- and some favorable headlines -- in Saudi Arabia and Israel on his first foreign tour, his political and possibly legal plight back home seemed to be inexorably worsening."




class Replace_Name_Place():
    '''
        Replaces name and places in ariticles with a placeholder 
        <NAME> or <PLACE>
        Reason: prevent mislead weight assignment for names and places
    '''

    def replace_name_place(self):
        name_holder = "<NAME>"
        place_holder = "<PLACE>"
        
        '''
        TODO-NEED TO LOOP TO RUN ALL DATASET
        '''
        #temorary usage
        raw_data = raw_test_data
        content = raw_data
        content = SpaceTokenizer().tokenize(content)   
        tags = ner_tagger.tag(content)
        
        person_list = []
        location_list = []
        
        for tag in tags:
            if(tag[1] == 'PERSON'): 
                person_list.append(tag[0])
            if(tag[1] == 'LOCATION'):
                location_list.append(tag[0])
        
        #Remove duplicate words
        person_list = list(set(person_list))
        location_list = list(set(location_list))
    
        for person in person_list:
            raw_data = raw_data.replace(person, name_holder)
              
        for location in location_list:
            raw_data = raw_data.replace(location, place_holder)
            
        print(raw_data)
        
#for testing
test = Replace_Name_Place()
test.replace_name_place()