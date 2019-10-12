def accuracy_tanshou(pred, target):
    correct_count = 0
    ndata = len(pred)
    for pred_row, target_row in zip(pred, target):
        pred1stidx = pred_row.index(1)
        target1stidx = target_row.index(1)
        if pred1stidx == target1stidx:
            correct_count += 1
    return correct_count/ndata

def accuracy_fukushou(pred, target):
    correct_count = 0
    ndata = len(pred)
    for pred_row, target_row in zip(pred, target):
        pred1stidx = pred_row.index(1)
        target1stidx = target_row.index(1)
        target2ndidx = target_row.index(2)
        target_idxs = [target1stidx, target2ndidx]
        if pred1stidx in target_idxs:
            correct_count += 1
    return correct_count/ndata

def accuracy_nirentan(pred, target):
    correct_count = 0
    ndata = len(pred)
    for pred_row, target_row in zip(pred, target):
        pred1stidx = pred_row.index(1)
        pred2ndidx = pred_row.index(2)
        target1stidx = target_row.index(1)
        target2ndidx = target_row.index(2)
        if target1stidx == pred1stidx and target2ndidx == pred2ndidx:
            correct_count += 1
    return correct_count/ndata

def accuracy_nirenfuku(pred, target):
    correct_count = 0
    ndata = len(pred)
    for pred_row, target_row in zip(pred, target):
        pred1stidx = pred_row.index(1)
        pred2ndidx = pred_row.index(2)
        target1stidx = target_row.index(1)
        target2ndidx = target_row.index(2)
        pred_idxs = [pred1stidx, pred2ndidx]
        if target1stidx in pred_idxs and target2ndidx in pred_idxs:
            correct_count += 1
    return correct_count/ndata

def accuracy_sanrentan(pred, target):
    correct_count = 0
    ndata = len(pred)
    for pred_row, target_row in zip(pred, target):
        pred1stidx = pred_row.index(1)
        pred2ndidx = pred_row.index(2)
        pred3rdidx = pred_row.index(3)
        target1stidx = target_row.index(1)
        target2ndidx = target_row.index(2)
        target3rdidx = target_row.index(3)
        if target1stidx == pred1stidx and target2ndidx == pred2ndidx and target3rdidx == pred3rdidx:
            correct_count += 1
    return correct_count/ndata

def accuracy_sanrenfuku(pred, target):
    correct_count = 0
    ndata = len(pred)
    for pred_row, target_row in zip(pred, target):
        pred1stidx = pred_row.index(1)
        pred2ndidx = pred_row.index(2)
        pred3rdidx = pred_row.index(3)
        target1stidx = target_row.index(1)
        target2ndidx = target_row.index(2)
        target3rdidx = target_row.index(3)
        pred_idxs = [pred1stidx, pred2ndidx, pred3rdidx]
        if target1stidx in pred_idxs and target2ndidx in pred_idxs and target3rdidx in pred_idxs:
            correct_count += 1
    return correct_count/ndata
