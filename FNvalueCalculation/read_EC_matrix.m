%plot_corrected_couplings('C:\Users\Administrator\Desktop\matalb-data\EC\1nh8.eij')
params = read_params('5mo4.eij');
figure
plot_coupling_scores(params);
saveas(gcf,'5mo4_eij.png');

export_couplings_json(read_params('5mo4.eij'), '5mo4_eij.json')
