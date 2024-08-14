python fit_signalshapes.py -M 200 250 300 \
  --inputFiles /vols/cms/jleonhol/l1scouting/zm200_filtered.h5 /vols/cms/jleonhol/l1scouting/zm250_filtered.h5 /vols/cms/jleonhol/l1scouting/zm300_filtered.h5 \
  --dcb-model \
  --fitRange 0.8 \
  -o ~/public_html/l1scouting/signal_shapes_eta
  #-o ~/public_html/l1scouting/signal_shapes
  #--inputFiles /vols/cms/jleonhol/l1scouting/zm200.h5 /vols/cms/jleonhol/l1scouting/zm250.h5 /vols/cms/jleonhol/l1scouting/zm300.h5 \
