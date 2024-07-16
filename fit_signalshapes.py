import argparse
import json
import os
import ROOT
from Utils import roundTo
from dijetfit import fit_signalmodel


def fit_signals(options):

    out_dir = os.path.abspath(options.outDir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    fine_bin_size = 5
    masses = options.masses
  
    binsx = [130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330, 350, 370, 390, 410,
             430, 450, 470, 490, 510, 530, 550, 570, 590, 610, 630, 650, 670, 690,
             710, 730, 750, 770, 790, 810, 830, 850, 870, 890, 910, 930, 950, 970]

    # round to smallest precision we are storing mass values with, otherwise
    # get weird effects related to bin size
    roundTo(binsx, fine_bin_size)
    bins_fine = int(binsx[-1]-binsx[0])/fine_bin_size

    if options.dcbModel:
        full_graphs = {'mean': ROOT.TGraphErrors(),
                       'sigma': ROOT.TGraphErrors(),
                       'alpha': ROOT.TGraphErrors(),
                       'alpha2': ROOT.TGraphErrors(),
                       'sign': ROOT.TGraphErrors(),
                       'sign2': ROOT.TGraphErrors()}
    else:
        full_graphs = {'mean': ROOT.TGraphErrors(),
                       'sigma': ROOT.TGraphErrors(),
                       'alpha': ROOT.TGraphErrors(),
                       'sign': ROOT.TGraphErrors(),
                       'scalesigma': ROOT.TGraphErrors(),
                       'sigfrac': ROOT.TGraphErrors()}

    for i, mass in enumerate(masses):
        print("########## FIT SIGNAL AND SAVE PARAMETERS ############")
        sig_file_name = os.path.join(out_dir, "sig_fit_{}.root".format(mass))
        plot_label = "M%i_" % mass
        current_fit = fit_signalmodel(options.inputFiles[i], sig_file_name,
                                      mass, binsx, bins_fine, out_dir + "/",
                                      return_fit=True, dcb_model=options.dcbModel, 
                                      fit_range = options.fitRange, plot_label = plot_label)

        parameters = dict()
        for var, graph in full_graphs.iteritems():
            val, err = current_fit.fetch(var)
            parameters[var] = val
            parameters['%s-err' % var] = err
            graph.SetPoint(i, mass, val)
            graph.SetPointError(i, 0.0, err)

        parameters["script_options"] = vars(options)
        sig_file_name = os.path.join(out_dir, "sig_fit_{}.json".format(mass))
        with open(sig_file_name, 'w') as f:
            json.dump(parameters, f, indent=4)
    
    full_file_name = os.path.join(out_dir, "full_fit.root")
    full_outfile = ROOT.TFile(full_file_name, "RECREATE")
    full_outfile.cd()

    for name, graph in full_graphs.iteritems():
        graph.Write(name)

    full_outfile.Close()


def fitting_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-M", "-M", dest="masses", type=int, nargs="+",
                        help="List of injected signal masses")
    parser.add_argument("-i", "--inputFiles", dest="inputFiles", nargs="+",
                        help="""List of input h5 files.
                        Must have same length as mass list""")
    parser.add_argument("-o", "--outDir", dest="outDir", default='plots/',
                        help="Where to store output files")
    parser.add_argument("--dcb-model", "--dcbModel", dest="dcbModel", action="store_true",
                        default=False,
                        help="Whether or not to use double crystal ball model")
    parser.add_argument("--fitRange", dest="fitRange", type = float, default=0.2,
                        help="What mass range to perform fit to signal shape over (in terms of frac. of signal mass)")
    return parser


if __name__ == "__main__":
    parser = fitting_options()
    options = parser.parse_args()
    fit_signals(options)
