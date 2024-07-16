#python dijetfit.py \
#  --mjj_min 200 --mjj_max 600 --sig_norm 0.000026 \
#  --sig_shape ZToQQ_shapes/sig_fit_300.root -M 300 \
#  --inputFile /eos/home-m/matteomi/l1ScoutingData/fitting/data/input1.h5 \
#  --dcb-model --scale_j_unc 0.1 --res_j_unc 0.035


python dijetfit.py --mjj_min 120 --mjj_max 600 --sig_norm 0.000026 --sig_shape ZToQQ_shapes/sig_fit_300.root -M 300 --inputFile data/input1.h5 --dcb-model --scale_j_unc 0.1 --res_j_unc 0.035 --fraction 0.01 --label "L1 Scouting Dijets" --nbinsx 25
