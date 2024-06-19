import pandapower as pp
import pandapower.networks as nw
import pandapower.plotting as plot
%matplotlib inline

net = nw.mv_oberrhein()
pp.runpp(net)