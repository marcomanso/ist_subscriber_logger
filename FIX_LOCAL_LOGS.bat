set ROOT_DIR="C:\Users\Marco\Downloads\EXPERIMENT_LOGS\EXPERIMENT_LOGS"

echo %ROOT_DIR%

python log_fixer.py --input %ROOT_DIR%\USA\20230818_baseline1_USA.log       --output %ROOT_DIR%\USA\20230818_baseline1_USA_fixed.log
python log_fixer.py --input %ROOT_DIR%\USA\20230818_baseline2_USA.log       --output %ROOT_DIR%\USA\20230818_baseline2_USA_fixed.log
python log_fixer.py --input %ROOT_DIR%\USA\20230818_high-frequency1_USA.log --output %ROOT_DIR%\USA\20230818_high-frequency1_USA_fixed.log
python log_fixer.py --input %ROOT_DIR%\USA\20230818_high-frequency2_USA.log --output %ROOT_DIR%\USA\20230818_high-frequency2_USA_fixed.log

python log_fixer.py --input %ROOT_DIR%\PRT_NOR\20230818_baseline1_prt.log   --output %ROOT_DIR%\PRT_NOR\20230818_baseline1_prt_fixed.log
python log_fixer.py --input %ROOT_DIR%\PRT_NOR\20230818_baseline2_prt.log   --output %ROOT_DIR%\PRT_NOR\20230818_baseline2_prt_fixed.log
python log_fixer.py --input %ROOT_DIR%\PRT_NOR\20230818_high_freq1_prt.log  --output %ROOT_DIR%\PRT_NOR\20230818_high_freq1_prt_fixed.log
python log_fixer.py --input %ROOT_DIR%\PRT_NOR\20230818_high_freq2_prt.log  --output %ROOT_DIR%\PRT_NOR\20230818_high_freq2_prt_fixed.log

python log_fixer.py --input %ROOT_DIR%\PRT_NOR\20230818_baseline1_nor.log   --output %ROOT_DIR%\PRT_NOR\20230818_baseline1_nor_fixed.log
python log_fixer.py --input %ROOT_DIR%\PRT_NOR\20230818_baseline2_nor.log   --output %ROOT_DIR%\PRT_NOR\20230818_baseline2_nor_fixed.log
python log_fixer.py --input %ROOT_DIR%\PRT_NOR\20230818_high_freq1_nor.log  --output %ROOT_DIR%\PRT_NOR\20230818_high_freq1_nor_fixed.log
python log_fixer.py --input %ROOT_DIR%\PRT_NOR\20230818_high_freq2_nor.log  --output %ROOT_DIR%\PRT_NOR\20230818_high_freq2_nor_fixed.log

python log_fixer.py --input %ROOT_DIR%\POL_DEU\logrun_pol_baseline_01_fri_18.log    --output %ROOT_DIR%\POL_DEU\logrun_pol_baseline_01_fri_18_fixed.log
python log_fixer.py --input %ROOT_DIR%\POL_DEU\logrun_pol_baseline_02_fri_18.log    --output %ROOT_DIR%\POL_DEU\logrun_pol_baseline_02_fri_18_18_fixed.log
python log_fixer.py --input %ROOT_DIR%\POL_DEU\logrun_pol_highfreq_03h_fri_18.log  --output %ROOT_DIR%\POL_DEU\logrun_pol_highfreq_03h_fri_18_fixed.log
python log_fixer.py --input %ROOT_DIR%\POL_DEU\logrun_pol_highfreq_04h_fri_18.log  --output %ROOT_DIR%\POL_DEU\logrun_pol_highfreq_04h_fri_18_fixed.log

python log_fixer.py --input %ROOT_DIR%\POL_DEU\logrun_deu_baseline_01_fri_18.log    --output %ROOT_DIR%\POL_DEU\logrun_deu_baseline_01_fri_18_fixed.log
python log_fixer.py --input %ROOT_DIR%\POL_DEU\logrun_deu_baseline_02_fri_18.log    --output %ROOT_DIR%\POL_DEU\logrun_deu_baseline_02_fri_18_18_fixed.log
python log_fixer.py --input %ROOT_DIR%\POL_DEU\logrun_deu_highfreq_03h_fri_18.log  --output %ROOT_DIR%\POL_DEU\logrun_deu_highfreq_03h_fri_18_fixed.log
python log_fixer.py --input %ROOT_DIR%\POL_DEU\logrun_deu_highfreq_04h_fri_18.log  --output %ROOT_DIR%\POL_DEU\logrun_deu_highfreq_04h_fri_18_fixed.log
