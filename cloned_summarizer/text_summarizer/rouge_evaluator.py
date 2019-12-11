# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 19:14:34 2019

@author: jairp

NOTES: 
    ROUGE-N: Overlap of N-grams[2] between the system and reference summaries.
        ROUGE-1 refers to the overlap of unigram (each word) between the system and reference summaries.
        ROUGE-2 refers to the overlap of bigrams between the system and reference summaries.
    ROUGE-L: Longest Common Subsequence (LCS)[3] based statistics.
        Longest common subsequence problem takes into account sentence level structure similarity 
        naturally and identifies longest co-occurring in sequence n-grams automatically.
    ROUGE-W: Weighted LCS-based statistics that favors consecutive LCSes .
    
"""

import rouge 

def prepare_results(p, r, f):
    """
    Formats and reports the in thw following format: 
        {metric} {Precision} {Recall} {F1 score}  
    """
    return '\t{}:\t{}: {:5.2f}\t{}: {:5.2f}\t{}: {:5.2f}'.format(
            'metric', 'P', 100.0 * p, 'R', 100.0 * r, 'F1', 100.0 * f)


def evaluate_hypotheses(hypotheses_list, references_list, 
                        criteria = ['Avg','Best','Individual'], 
                        metrics = ['rouge-n', 'rouge-l', 'rouge-w']): 
    
    # Evaluate using all of the followign criteria
    for aggregator in criteria: 
        
        # Choose which evaluation criterion to apply 
        print('Evaluation with {}'.format(aggregator))
        apply_avg = aggregator == 'Avg'
        apply_best = aggregator == 'Best'
        
        
        evaluator = rouge.Rouge(metrics = metrics, # Types of rouge metrics to evaluate 
                               max_n=4, # max number of unigrams to consider  
                               limit_length=True, # If the summaries must be truncated. (default = True)
                               length_limit=100, # Number of the truncation where the unit is express int length_limit_Type.
                               length_limit_type='words', # Unit of length_limit. Available: words, bytes. Default: 'bytes' 
                               apply_avg=apply_avg, # If we should average the score of multiple samples. 
                               apply_best=apply_best, # Take the best instead of the average. Default: False, then each ROUGE scores are independant
                               alpha=0.5, # Alpha use to compute f1 score: P*R/((1-a)*P + a*R). Default:0.5
                               weight_factor=1.2, # Weight factor to be used for ROUGE-W. Official rouge score defines it at 1.2. Default: 1.0
                               stemming=True # apply stemming to the testing data 
                               )
        
        scores = evaluator.get_scores(hypotheses_list, all_references)  
        
        for metric, results in sorted(scores.items(), key=lambda x: x[0]):
            if not apply_avg and not apply_best: # value is a type of list as we evaluate each summary vs each reference
                for hypothesis_id, results_per_ref in enumerate(results):
                    nb_references = len(results_per_ref['p'])
                    for reference_id in range(nb_references):
                        print('\tHypothesis #{} & Reference #{}: '.format(hypothesis_id, reference_id))
                        print('\t' + prepare_results(results_per_ref['p'][reference_id], results_per_ref['r'][reference_id], results_per_ref['f'][reference_id]))
                print()
            else:
                print(prepare_results(results['p'], results['r'], results['f']))
        print()
        
        
    
## TESTS ### 

# The input hypotheses and references must be of this format 
        
hypothesis_1 = "King Norodom Sihanouk has declined requests to chair a summit of Cambodia 's top political leaders , saying the meeting would not bring any progress in deadlocked negotiations to form a government .\nGovernment and opposition parties have asked King Norodom Sihanouk to host a summit meeting after a series of post-election negotiations between the two opposition groups and Hun Sen 's party to form a new government failed .\nHun Sen 's ruling party narrowly won a majority in elections in July , but the opposition _ claiming widespread intimidation and fraud _ has denied Hun Sen the two-thirds vote in parliament required to approve the next government .\n"
references_1 = ["Prospects were dim for resolution of the political crisis in Cambodia in October 1998.\nPrime Minister Hun Sen insisted that talks take place in Cambodia while opposition leaders Ranariddh and Sam Rainsy, fearing arrest at home, wanted them abroad.\nKing Sihanouk declined to chair talks in either place.\nA U.S. House resolution criticized Hun Sen's regime while the opposition tried to cut off his access to loans.\nBut in November the King announced a coalition government with Hun Sen heading the executive and Ranariddh leading the parliament.\nLeft out, Sam Rainsy sought the King's assurance of Hun Sen's promise of safety and freedom for all politicians.",
                "Cambodian prime minister Hun Sen rejects demands of 2 opposition parties for talks in Beijing after failing to win a 2/3 majority in recent elections.\nSihanouk refuses to host talks in Beijing.\nOpposition parties ask the Asian Development Bank to stop loans to Hun Sen's government.\nCCP defends Hun Sen to the US Senate.\nFUNCINPEC refuses to share the presidency.\nHun Sen and Ranariddh eventually form a coalition at summit convened by Sihanouk.\nHun Sen remains prime minister, Ranariddh is president of the national assembly, and a new senate will be formed.\nOpposition leader Rainsy left out.\nHe seeks strong assurance of safety should he return to Cambodia.\n",
                ]

hypothesis_2 = "China 's government said Thursday that two prominent dissidents arrested this week are suspected of endangering national security _ the clearest sign yet Chinese leaders plan to quash a would-be opposition party .\nOne leader of a suppressed new political party will be tried on Dec. 17 on a charge of colluding with foreign enemies of China '' to incite the subversion of state power , '' according to court documents given to his wife on Monday .\nWith attorneys locked up , harassed or plain scared , two prominent dissidents will defend themselves against charges of subversion Thursday in China 's highest-profile dissident trials in two years .\n"
references_2 = "Hurricane Mitch, category 5 hurricane, brought widespread death and destruction to Central American.\nEspecially hard hit was Honduras where an estimated 6,076 people lost their lives.\nThe hurricane, which lingered off the coast of Honduras for 3 days before moving off, flooded large areas, destroying crops and property.\nThe U.S. and European Union were joined by Pope John Paul II in a call for money and workers to help the stricken area.\nPresident Clinton sent Tipper Gore, wife of Vice President Gore to the area to deliver much needed supplies to the area, demonstrating U.S. commitment to the recovery of the region.\n"

all_hypothesis = [hypothesis_1, hypothesis_2]
all_references = [references_1, references_2]

# Run the Rouge-score evaluation on the test data
evaluate_hypotheses(all_hypothesis, all_references)
    
    
    