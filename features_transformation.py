from nltk.tokenize import SpaceTokenizer
from nltk.tag.stanford import StanfordPOSTagger #StanfordNERTagger

#NEED TO SET ENV FOR PROJECT LATER

jar = "libs/stanford-postagger-3.7.0.jar"
model = "libs/english-left3words-distsim.tagger"

#POST TAGGER NOT WORK FOR NAME

pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')

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
    name = "<NAME>"
    place = "<PLACE>"
    
    def replace_name_place(self):
        '''
        TODO-NEED TO LOOP TO RUN ALL DATASET
        '''
        #temorary usage
        content = raw_test_data
        content = SpaceTokenizer().tokenize(content)   
        tags = pos_tagger.tag(content)
        
        for tag in tags:
            print(tag)

#for testing
test = Replace_Name_Place()
test.replace_name_place()