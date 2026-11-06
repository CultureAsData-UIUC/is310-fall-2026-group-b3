"""Check the supplied CSV against its saved responses. No network access."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
import collect_big_ten as collector

BASE = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--details", action="store_true", help="Also save the detailed comparison CSV and draft annotations")
    args = parser.parse_args()
    rows = list(csv.DictReader((BASE / 'big_ten_2024_25.csv').open(encoding='utf-8-sig')))
    errors = []
    expected = {(s, m) for s, _, _ in collector.SCHOOLS for m in collector.METRICS}
    keys = [(r['school'], r['measure']) for r in rows]
    if len(rows) != 72 or len(set(keys)) != 72 or set(keys) != expected:
        errors.append('Missing or duplicate school/measure pairs')
    checks = []
    annotations = []
    for school, unit_id, profile in collector.SCHOOLS:
        e = json.loads((BASE/'source_cache'/f'eada_{unit_id}.json').read_text())
        k = json.loads((BASE/'source_cache'/f'knight_{unit_id}.json').read_text())
        ev, header, es = collector.eada_values(e, unit_id)
        kv, ks = collector.knight_values(k)
        if es != 'ok' or ks != 'ok': errors.append(f'{school}: source parsing status {es}/{ks}')
        raw = json.loads(e['body'])
        caveats = []
        for group in raw['Groups']:
            for screen in group['Screens']:
                for row in screen['Rows']:
                    if len(row['Cells']) == 1:
                        text = collector.plain(row['Cells'][0]['Html'])
                        if text and text != 'CAVEAT': caveats.append({'screen':screen['ScreenName'],'text':text})
        for r in [r for r in rows if r['school'] == school]:
            metric = r['measure']
            for source, values, key in [('EADA',ev,'eada_amount_usd'),('Knight-Newhouse',kv,'knight_amount_usd')]:
                value = values.get(metric)
                actual = '' if value is None else str(int(value))
                match = r[key] == actual
                checks.append({'school':school,'measure':metric,'source':source,'csv_value':r[key], 'saved_response_value':actual,'result':'match' if match else 'MISMATCH'})
                if not match: errors.append(f'{school}/{metric}/{source}: amount differs')
                if bool(r[key]) != (r['eada_status' if source=='EADA' else 'knight_status']=='collected'):
                    errors.append(f'{school}/{metric}/{source}: status and amount disagree')
            if r['eada_period_start'] != str(header['ReportingYearStart'])[:10] or r['eada_period_end'] != str(header['ReportingYearEnd'])[:10]:
                errors.append(f'{school}: dates differ from saved response')
            if r['knight_year_label'] != '2025': errors.append(f'{school}: wrong Knight year')
            decision = 'contextual_comparison_only'
            reasons = ['EADA and NCAA MFRS are different reporting systems; a dollar difference alone does not establish error.']
            if not r['knight_amount_usd']:
                decision = 'no_numeric_comparison'
                reasons.append('Selected Knight profile lacks the requested figure; leave blank rather than enter zero.')
            if metric.startswith('football'):
                reasons.append('Football is a component of department activity; do not add it to department totals.')
            if metric == 'total_athletic_revenue':
                reasons.append('Revenue is not profit or evidence of a payment to athletes; exact category reconciliation remains open.')
            if r['eada_period_start'] != '2024-07-01' or r['eada_period_end'] != '2025-06-30':
                reasons.append('Non-July–June EADA period; Knight school-specific dates have not been verified.')
            else:
                reasons.append('Year labels plausibly align, but exact Knight school-specific reporting dates remain unverified.')
            annotations.append({'school':school,'measure':metric,'comparison_decision':decision,'interpretation':reasons,
                                'eada_period_start':r['eada_period_start'],'eada_period_end':r['eada_period_end'],
                                'school_caveats_from_saved_response':caveats,
                                'authorship':'AI-assisted draft for me to review',
                                'verification_scope':'CSV checked against supplied cached responses using collector parser; original university reports not checked',
                                'eada_source':r['eada_source'],'knight_source':r['knight_source']})
    if args.details:
        with (BASE/'source_checks.csv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=list(checks[0]));writer.writeheader();writer.writerows(checks)
        (BASE/'audit_annotations.json').write_text(json.dumps(annotations,indent=2,ensure_ascii=False)+'\n')
    lines=[f'Records: {len(rows)}',f'Institutions: {len(set(r["school"] for r in rows))}',
           f'Unique school/measure pairs: {len(set(keys))}',
           f'EADA reported amounts: {sum(bool(r["eada_amount_usd"]) for r in rows)}',
           f'Knight reported amounts: {sum(bool(r["knight_amount_usd"]) for r in rows)}',
           f'Saved-response comparisons: {len(checks)} (includes missing values)',
           f'Matching comparisons: {sum(c["result"]=="match" for c in checks)}',
           'Non-July–June school: '+', '.join(sorted({r['school'] for r in rows if r['eada_period_start']!='2024-07-01' or r['eada_period_end']!='2025-06-30'})),
           'Knight missing-value statuses: '+str(dict(Counter(r['knight_status'] for r in rows if not r['knight_amount_usd']))),
           f'Errors: {len(errors)}',*errors,
           'LIMIT: Matching a cached response is not independent verification of the underlying university report.',
           'LIMIT: The same collector parser is reused for these extraction checks.',
           'LIMIT: Audit annotations are AI-assisted drafts, not a claim that I manually reviewed every record.']
    report='\n'.join(lines)+'\n'
    (BASE/'validation_output.txt').write_text(report)
    print(report)
    if errors: raise SystemExit(1)

if __name__=='__main__': main()
