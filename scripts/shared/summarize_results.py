"""Full-13 model/prompt summaries and ordinal confidence versus correctness."""
import pandas as pd
from scripts.shared.paths import ROOT, generated_path

def main():
    metrics=pd.read_csv(generated_path('results/rq1/metrics/effectiveness_by_run.csv'))
    names=['precision','recall','F1','MCC','specificity','balanced_accuracy','accuracy']
    overall=metrics[(metrics.level=='overall') & (metrics.model!='AQUSA')]
    config=overall.groupby(['model','prompt_profile'])[names].mean()
    for key in ['model','prompt_profile']:
        config.groupby(key)[names].mean().to_csv(generated_path('results/rq1/tables/summary_by_'+key+'.csv'))
    data=pd.read_csv(generated_path('outputs/parsed/normalized/llm_predictions.csv'),keep_default_na=False)
    ref=pd.read_csv(ROOT/'data/ground_truth/gold_standard_qus13_final.csv',keep_default_na=False)
    ref=ref[['project','story_id','qus_criterion','decision']].rename(columns={'qus_criterion':'criterion','decision':'ground_truth'})
    data=data.merge(ref,on=['project','story_id','criterion'],validate='many_to_one')
    assert len(data)==106470
    data['correct']=data.decision.eq(data.ground_truth)
    for name,keys in [('overall',['confidence']),('model',['model','confidence']),('prompt',['prompt_profile','confidence']),('criterion',['criterion','confidence'])]:
        out=data.groupby(keys).correct.agg(total='size',correct='sum',accuracy='mean').reset_index()
        out['incorrect']=out.total-out.correct
        out.to_csv(generated_path('results/rq3/tables/confidence_by_'+name+'.csv'),index=False)

if __name__=='__main__':main()
