#!/usr/bin/env bats

@test "hist total_energy" {
diff <(abcd hist total_energy) - <<EOF
                -449910.248128 893
           -427415.27682367887 24
            -404920.3055193577 0
            -382425.3342150365 0
           -359930.36291071534 0
            -337435.3916063942 0
             -314940.420302073 0
            -292445.4489977518 0
            -269950.4776934307 0
            -247455.5063891095 0
           -224960.53508478834 0
           -202465.56378046717 1224
             -179970.592476146 0
            -157475.6211718248 0
           -134980.64986750367 0
           -112485.67856318253 0
            -89990.70725886134 0
            -67495.73595454014 0
           -45000.764650219004 10300
           -22505.793345897866 46671
EOF
}

@test "hist config_type" {
diff <(abcd hist config_type) - <<EOF
              bcc_bulk_54_high 28
    bcc_doublevacancy_126_high 78
      bcc_monovacancy_127_high 57
        dislocation_quadrupole 100
    doublevacancy_126_1NN_high 46
    doublevacancy_126_2NN_high 48
                 gamma_surface 18549
             gamma_surface_110 5000
             gamma_surface_112 4898
         gamma_surface_vacancy 1500
                       md_bulk 300
           monovacancy_53_high 762
              phonons_128_high 180
               phonons_54_high 434
          quadvacancy_124_high 28
          quinvacancy_123_high 24
self_di_interstitial_npc_130_high 36
    self_interstitial_100_high 42
    self_interstitial_110_high 24
    self_interstitial_111_high 74
    self_interstitial_oct_high 32
    self_interstitial_tet_high 50
    self_interstitial_xxy_high 48
                  slice_sample 12000
             slice_sample_high 12002
                       surface 540
                   surface_100 110
                   surface_110 98
                   surface_111 86
                   surface_211 108
       trivacancy_100_125_high 30
       trivacancy_110_125_high 62
       trivacancy_111_125_high 58
                       vacancy 1680
EOF
}
