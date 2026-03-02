def confusion_matrix(true_labels, pred_labels):
    labels = sorted(set(true_labels) | set(pred_labels))
    idx = {lab: i for i, lab in enumerate(labels)}
    matrix = [[0 for _ in labels] for _ in labels]
    for t, p in zip(true_labels, pred_labels):
        matrix[idx[t]][idx[p]] += 1
    return labels, matrix

def precision_recall_f1(true_labels, pred_labels):
    tp = sum(1 for t, p in zip(true_labels, pred_labels) if t == p)
    accuracy = tp / len(true_labels) if true_labels else 0.0

    labels = sorted(set(true_labels) | set(pred_labels))
    per_label = {}
    for lab in labels:
        tp_lab = sum(1 for t, p in zip(true_labels, pred_labels) if t == lab and p == lab)
        fp_lab = sum(1 for t, p in zip(true_labels, pred_labels) if t != lab and p == lab)
        fn_lab = sum(1 for t, p in zip(true_labels, pred_labels) if t == lab and p != lab)
        prec = tp_lab / (tp_lab + fp_lab) if (tp_lab + fp_lab) > 0 else 0.0
        rec = tp_lab / (tp_lab + fn_lab) if (tp_lab + fn_lab) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
        per_label[lab] = {"precision": prec, "recall": rec, "f1": f1}

    return {"accuracy": accuracy, "per_label": per_label}
