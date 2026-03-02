import csv, json, os
from .model_client import ModelClient
from .metrics import confusion_matrix, precision_recall_f1

def load_test_cases(path: str):
    cases = []
    with open(path, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            cases.append(row)
    return cases

def load_gold(path: str):
    gold = {}
    with open(path, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            gold[row['case_id']] = row['expected_label']
    return gold

def run_evaluation(test_cases_path: str, gold_path: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    cases = load_test_cases(test_cases_path)
    gold = load_gold(gold_path)

    client = ModelClient()

    y_true, y_pred, rows = [], [], []
    scenarios = {}  # scenario -> list of (true, pred)

    for c in cases:
        cid = c['case_id']
        inp = c['input_text']
        scenario = c.get('scenario', 'unspecified')
        pred = client.predict(inp)
        true = gold.get(cid)
        y_true.append(true)
        y_pred.append(pred)
        rows.append({
            'case_id': cid,
            'scenario': scenario,
            'input_text': inp,
            'gold_label': true,
            'pred_label': pred,
            'match': str(true == pred)
        })
        scenarios.setdefault(scenario, {'y_true': [], 'y_pred': []})
        scenarios[scenario]['y_true'].append(true)
        scenarios[scenario]['y_pred'].append(pred)

    # Global metrics
    labels, cm = confusion_matrix(y_true, y_pred)
    pr = precision_recall_f1(y_true, y_pred)
    metrics = {
        'labels': labels,
        'confusion_matrix': cm,
        'summary': pr,
        'by_scenario': {}
    }

    # Scenario metrics
    for scn, pairs in scenarios.items():
        scn_pr = precision_recall_f1(pairs['y_true'], pairs['y_pred'])
        metrics['by_scenario'][scn] = scn_pr

    # Write outputs
    with open(os.path.join(out_dir, 'metrics.json'), 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)

    # Row-level report
    with open(os.path.join(out_dir, 'evaluation_report.csv'), 'w', newline='', encoding='utf-8') as f:
        fieldnames = list(rows[0].keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    return metrics
