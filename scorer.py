#!/usr/bin/env python3
"""
Site Evaluation Comprehensive Scoring Engine
Reads form responses, applies the rubric, and calculates detailed scores
"""

from googleapiclient import discovery

API_KEY = 'AIzaSyBVqH00y4Ta4Iw5oavrkdP3e04ixJOtL_M'
FORM_SPREADSHEET_ID = '1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY'
RUBRIC_SPREADSHEET_ID = '1vLwSqajfazSB8OYBJhK_OEwn2w5xVB-gbTsh_VjBMVI'

class SiteEvaluationScorer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.service = discovery.build('sheets', 'v4', developerKey=api_key)
        self.responses = None
        self.headers = None
        
        # Define link fields that should be captured for each category
        # Maps link name to (category, item_name, data_index)
        self.link_fields = {
            'PBMC Lab Photos': {
                'category': 'Phase Capabilities',
                'item_name': 'PBMC',
                'index': 18
            },
            'Coordinator Certifications': {
                'category': 'Key Personnel',
                'item_name': 'Certified Coordinators',
                'index': 22
            }
        }
        
        # Define the scoring rules based on the rubric
        self.scoring_rules = {
            'Studies enrolling': {
                'header_index': 1,
                'category': 'Study Capabilities',
                'rule': lambda x: {
                    0: -10, 1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 5
                }.get(x, 5)
            },
            'Active studies': {
                'header_index': 3,
                'category': 'Study Capabilities',
                'rule': lambda x: {
                    0: -3, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 1
                }.get(x, 1)
            },
            'Inpatient': {
                'header_index': 11,
                'category': 'Phase Capabilities',
                'rule': lambda x: 3 if x.lower() == 'yes' else 0
            },
            'PK/PD': {
                'header_index': 12,
                'category': 'Phase Capabilities',
                'rule': lambda x: 1 if x.lower() == 'yes' else 0
            },
            'Phase 2-4': {
                'header_index': 13,
                'category': 'Phase Capabilities',
                'rule': lambda x: 1 if str(x).lower() == 'yes' else 0
            },
            'High-volume': {
                'header_index': 15,
                'category': 'Phase Capabilities',
                'rule': lambda x: 1 if x.lower() == 'yes' else 0
            },
            'PBMC': {
                'header_index': 17,
                'category': 'Phase Capabilities',
                'rule': lambda x: 1 if x.lower() == 'yes' else 0
            },
            'NIH Studies': {
                'header_index': 19,
                'category': 'Phase Capabilities',
                'rule': lambda x: 1 if x.lower() == 'yes' else 0
            },
            'Total Coordinators': {
                'header_index': 20,
                'category': 'Key Personnel',
                'rule': lambda x: {
                    0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 2
                }.get(x, 2)
            },
            'Certified Coordinators': {
                'header_index': 21,
                'category': 'Key Personnel',
                'rule': lambda x: {
                    0: 0, 1: 0, 2: 2, 3: 2, 4: 4, 5: 4
                }.get(x, 4)
            },
            'Total Investigators': {
                'header_index': 23,
                'category': 'Key Personnel',
                'rule': lambda x: {
                    0: -2, 1: -2, 2: -2, 3: 0, 4: 0, 5: 2, 6: 2
                }.get(x, 2)
            },
            'Active Investigators': {
                'header_index': 24,
                'category': 'Key Personnel',
                'rule': lambda x: {
                    0: -3, 1: 0, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3
                }.get(x, 3)
            },
            'Experienced Investigators': {
                'header_index': 25,
                'category': 'Key Personnel',
                'rule': lambda x: {
                    0: 0, 1: 1, 2: 2, 3: 2
                }.get(x, 2)
            },
        }
    
    def load_responses(self, spreadsheet_id, sheet_name='Responses_Raw'):
        """Load form responses"""
        print(f"Loading responses from {sheet_name}...")
        
        result = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f'{sheet_name}!A1:DZ100'
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print("No responses found")
            return False
        
        self.headers = values[0]
        self.responses = values[1:]
        
        print(f"✓ Loaded {len(self.responses)} response(s)\n")
        return True
    
    def extract_number(self, value):
        """Extract numeric value from a string"""
        try:
            # If it's already a number
            if isinstance(value, (int, float)):
                return int(value)
            # Extract first number from string
            import re
            match = re.search(r'\d+', str(value).strip())
            return int(match.group()) if match else 0
        except:
            return 0
    
    def score_response(self, response, response_num):
        """Score a single response based on the rubric"""
        scores_by_category = {
            'Study Capabilities': [],
            'Phase Capabilities': [],
            'Key Personnel': []
        }
        
        print(f"\nScoring Response #{response_num}:")
        print("-" * 70)
        
        for item_name, rule_config in self.scoring_rules.items():
            idx = rule_config['header_index']
            category = rule_config['category']
            rule_func = rule_config['rule']
            
            if idx < len(response):
                value = response[idx].strip() if response[idx] else '0'
                
                try:
                    # Extract numeric value or use as-is
                    if isinstance(value, str) and value.lower() in ['yes', 'no']:
                        points = rule_func(value)
                    else:
                        numeric_value = self.extract_number(value)
                        points = rule_func(numeric_value)
                except Exception as e:
                    print(f"  ⚠ Error scoring {item_name}: {e}")
                    points = 0
                
                score_item = {
                    'item': item_name,
                    'value': value,
                    'points': points,
                    'link': None
                }
                
                # Check if this item has an associated link
                for link_name, link_info in self.link_fields.items():
                    if link_info['item_name'] == item_name and link_info['category'] == category:
                        link_idx = link_info['index']
                        if link_idx < len(response):
                            link_value = response[link_idx].strip() if response[link_idx] else ''
                            if link_value:
                                score_item['link'] = {
                                    'name': link_name,
                                    'url': link_value
                                }
                
                scores_by_category[category].append(score_item)
                
                print(f"  {item_name:30} | Value: {value:15} | Points: {points:+3}")
        
        # Calculate totals
        category_totals = {}
        total_score = 0
        
        print("\nCategory Totals:")
        for category, items in scores_by_category.items():
            cat_total = sum(item['points'] for item in items)
            category_totals[category] = cat_total
            total_score += cat_total
            print(f"  {category:30} | {cat_total:+4} points")
        
        print("-" * 70)
        print(f"  TOTAL SCORE: {total_score}")
        print()
        
        return {
            'response_num': response_num,
            'items': scores_by_category,
            'category_totals': category_totals,
            'total_score': total_score
        }
    
    def process_all_responses(self):
        """Process and score all responses"""
        print("=" * 70)
        print("SITE EVALUATION SCORING")
        print("=" * 70)
        
        all_scores = []
        for i, response in enumerate(self.responses, 1):
            score = self.score_response(response, i)
            all_scores.append(score)
        
        return all_scores
    
    def print_summary(self, all_scores):
        """Print summary of all scores"""
        print("\n" + "=" * 70)
        print("SCORING SUMMARY")
        print("=" * 70)
        
        for score in all_scores:
            print(f"\nResponse #{score['response_num']}:")
            print(f"  Study Capabilities: {score['category_totals']['Study Capabilities']:+4}")
            print(f"  Phase Capabilities: {score['category_totals']['Phase Capabilities']:+4}")
            print(f"  Key Personnel:      {score['category_totals']['Key Personnel']:+4}")
            print(f"  TOTAL:              {score['total_score']:+4}")


def main():
    scorer = SiteEvaluationScorer(API_KEY)
    
    # Load responses
    if not scorer.load_responses(FORM_SPREADSHEET_ID):
        return
    
    # Score them
    scores = scorer.process_all_responses()
    
    # Print summary
    scorer.print_summary(scores)
    
    print("\n✓ Scoring complete!")
    
    return scores


if __name__ == '__main__':
    main()
