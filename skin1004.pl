% Fakta: rekomendasi produk berdasarkan tipe kulit, masalah kulit, dan preferensi
rekomendasi(kering, dehidrasi, natural, [
    'SKIN1004 Hyalu-Cica Brightening Toner',
    'SKIN1004 Hyalu-Cica Blue Serum',
    'SKIN1004 Hyalu-Cica Moisture Cream'
]).

rekomendasi(berminyak, jerawat, kimiawi, [
    'SKIN1004 Tea-Trica BHA Foam',
    'SKIN1004 Tea-Trica Toner',
    'SKIN1004 Tea-Trica Spot Cream'
]).

rekomendasi(sensitif, iritasi, natural, [
    'SKIN1004 Centella Ampoule Foam',
    'SKIN1004 Centella Toning Toner',
    'SKIN1004 Centella Ampoule'
]).

rekomendasi(normal, penuaan, kimiawi, [
    'SKIN1004 Madagascar Centella Probio-Cica Serum',
    'SKIN1004 Tone Brightening Capsule Cream'
]).

rekomendasi(_, _, _, [
    'SKIN1004 Basic Cleansing Oil',
    'SKIN1004 Centella Ampoule',
    'SKIN1004 Sunscreen SPF50+ PA++++'
]).
