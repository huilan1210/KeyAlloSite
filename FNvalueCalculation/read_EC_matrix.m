%plot_corrected_couplings('C:\Users\Administrator\Desktop\matalb-data\EC\1nh8.eij')
params = read_params('3lcb.eij');
figure
plot_coupling_scores(params);
saveas(gcf,'3lcb_eij.png');

export_couplings_json(read_params('3lcb.eij'), '3lcb_eij.json')