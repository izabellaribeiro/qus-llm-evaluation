"""Summarize final ratings without re-rating or changing sample membership."""
import json
import pandas as pd
from scripts.shared.paths import ROOT, generated_path

def main():
    cases=pd.read_excel(ROOT/'data/qualitative_sample/final_coding.xlsx',sheet_name='Final Coding')
    ref=pd.read_csv(ROOT/'data/ground_truth/gold_standard_qus13_final.csv').set_index(['project','story_id','qus_criterion']).decision
    assert len(cases)==30 and cases['Case ID'].is_unique
    for _,r in cases.iterrows():
        gt=ref.loc[(r.Project,r['Story ID'],r['QUS Criterion'])]
        assert gt==r['Ground Truth']
        expected=('TP' if r['LLM Decision']=='Violation' else 'FN') if gt=='Violation' else ('FP' if r['LLM Decision']=='Violation' else 'TN')
        assert expected==r.Quadrant
    out=generated_path('results/rq4');out.mkdir(parents=True,exist_ok=True)
    cases.to_csv(out/'final_coding.csv',index=False)
    rows=[]
    for group,f in [('all',cases),('correct',cases[cases.Quadrant.isin(['TP','TN'])]),('incorrect',cases[cases.Quadrant.isin(['FP','FN'])])]:
        row={'group':group,'n':len(f)}
        for dimension in ['RC','ES']:
            for score in range(3):row[dimension+str(score)]=int(f['Final '+dimension].str.startswith(dimension+str(score)).sum())
        rows.append(row)
    pd.DataFrame(rows).to_csv(out/'rating_counts.csv',index=False)
    agreement=[]
    for dimension in ['RC','ES']:
        a=cases['Coder 1 '+dimension].str[2].astype(int);b=cases['Coder 2 '+dimension].str[2].astype(int)
        observed=((a-b)**2).mean();expected=sum((a.eq(i).mean()*b.eq(j).mean()*(i-j)**2) for i in range(3) for j in range(3))
        agreement.append({'dimension':dimension,'n':len(cases),'exact_agreement':float(a.eq(b).mean()),'quadratic_weighted_kappa':1-observed/expected if expected else None,'scope':'Descriptive agreement after author-reported Q15/Q30 confirmation; not original independent pre-adjudication agreement'})
    pd.DataFrame(agreement).to_csv(out/'current_rater_agreement.csv',index=False)
    (out/'quadrants.json').write_text(json.dumps(cases.Quadrant.value_counts().to_dict(),indent=2)+'\n')

if __name__=='__main__':main()
