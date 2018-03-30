
values_bounds = {
    'electrolisys': {
        'lodas': (0, 20),
        'fact': (0, 1000),
    },
    'pulp': {
        'zn_pulp': {
            'ph': (0, 10),
            'temp': (0, 150),
        },
        'cu_pulp': {
            'before': (0, 10),
            'after': (0, 50),
            'tv': (0, 1000),
        },
        'fe_solution': {
            'h2so4': (0, 20),
            'tv': (0, 10),
            'sb': (0, 50),
            'cu': (500, 2500),
            'fe': (100, 1000),
            'density': (0, 20),
            'as': (0, 20),
            'cl': (0, 10),
        },
        'daily_anal': {
            'sb_in_shlippe': (0, 200),
            'sas_activity': (0, 200),
            'high_fe': (0, 200)
        },
    },
    'densers': {
        'ph': (0, 10),
        'cu': (500, 2500),
        'fe': (0, 500)
    },
    'hydrometal': {
        '1': {
            'ph': (0, 10),
            'acidity': (0, 200),
            'fe2': (0, 1000),
            'fe_total': (500, 2500),
        },
        '4': {
            'ph': (0, 10),
            'cu': (500, 2500),
            'fe2': (0, 100),
            'sb': (0, 10),
            'sediment': (0, 20),
        },
        'sieve': {
            'cinder_sieve': (0, 20),
            'cinder_sieve_avg': (0, 20),
            'fe_total': (100, 2500),
            'fe_shave': (0, 20)
        }
    },
    'hydrometal2': {
        'ready_solution': {
            'h2so4': (0, 100),
            'cu': (0, 2500),
        },
        'refining_agitators': {
            'cu': (0, 2500),
            'co': (0, 200),
            'cd': (0, 50),
            'ph': (0, 10),
        }
    },
    'top_block': {
        'hsls': {
            'co': (0, 20),
            'sb': (0, 10),
            'cu_hsls': (500, 3000),
            'cu_1_st': (50, 1000),
            'cd_bchc': (500, 1500),
            'sol_1_st': (0, 10),
            'ph': (0, 10),
            'fe': (0, 100),
            'as': (0, 10),
            'sol': (0, 10),
            'density': (500, 2000)
        },
        'larox': {
            'co': (0, 10),
            'sb': (0, 10),
            'cd': (0, 50),
            'sol': (0, 500),
            'ph': (0, 10),
        },
        'purified_solution': {
            'co': (0, 10),
            'sb': (0, 10),
            'cd': (0, 10),
            'cu': (0, 10),
            'fe': (0, 200),
            'current_output': (0, 200),
            'density': (0, 200),
        },
        'product_errors': {
            'norm': (0, 200),
            'fact': (0, 200),
        }
    },
    'neutral_densers': {
        'sediment': (0, 500)
    },
    'ready_product': {
        'cd': (0, 10),
        'cu': (0, 10),
        'co': (0, 10),
        'sb': (0, 10),
        'fe': (0, 150),
        'vt': (0, 500),
        'density': (0, 2500),
        'norm': (0, 2500),
        'fact': (0, 2500),
        'correction': (0, 10),
    },
    'tanks': {
        'prev_mjr': {
            'all_tanks': (0, 2000),
            'shift_balance': (0, 6000),
            'day_balance': (0, 6000),
        },
        'curr_mjr': {
            'all_tanks': (0, 2000),
            'shift_balance': (0, 6000),
            'day_balance': (0, 6000),
        },
        'deviation': {
            'all_tanks': (-1000, 1000),
            'shift_balance': (-1000, 1000),
            'day_balance': (-1000, 1000),
        }
    },
    'shift_info': {
        'cu_cake': (0, 5000),
        'recycles_cvoc': (0, 2500),
        'cd_rich': (0, 1500),
        'neutral': (0, 200),
        'cu_pulp': (0, 200),
        'density': (0, 200),
        'fe_cvoc': (0, 2500),
        'high_fe_cvoc': (0, 2500),
        'poor_cd': (0, 2500),
    },
    'sample2': {
        'cd': (0, 2500),
        'cu': (0, 2500),
    }
}
