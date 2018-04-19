
values_bounds = {
    'electrolisys': {
        'lodas': (0, 20),
        'fact': (0, 1000),
    },
    'pulp': {
        'zn_pulp': {
            'ph': (0, 10),
            't0': (0, 150),
        },
        'cu_pulp': {
            'before': (0, 10),
            'after': (0, 50),
            'solid': (0, 1000),
        },
        'fe_solution': {
            'h2so4': (0, 20),
            'solid': (0, 10),
            'sb': (0, 50),
            'cu': (500, 2500),
            'fe': (100, 1000),
            'density': (0, 20),
            'arsenic': (0, 20),
            'cl': (0, 10),
        },
        'daily_anal': {
            'shlippe_sb': (0, 200),
            'activ_sas': (0, 200),
            # 'high_fe': (0, 200)
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
            'acid': (0, 200),
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
            'gran': (0, 20),
            'gran_avg': (0, 20),
            'fe_avg': (100, 2500),
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
            'cu': (500, 3000),
            'cu_st1': (50, 1000),
            'cd': (500, 1500),
            'solid_st1': (0, 10),
            'ph': (0, 10),
            'fe': (0, 100),
            'arsenic': (0, 10),
            'solid': (0, 10),
            'density': (500, 2000)
        },
        'larox': {
            'co': (0, 10),
            'sb': (0, 10),
            'cd': (0, 50),
            'sol': (0, 500),
            'ph': (0, 10),
        },
        'purified': {
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
        'prev_measure': (0, 2000),
        'cur_measure': (0, 2000),
        'deviation': (-1000, 1000),
    },
    'shift_info': {
        'out_cu_kek': (0, 5000),
        'out_electr': (0, 2500),
        'out_ruch_cd': (0, 1500),
        'out_neutr': (0, 200),
        'out_cu_pulp': (0, 200),
        'in_fe': (0, 2500),
        'in_fe_hi': (0, 2500),
        'in_poor_cd': (0, 2500),
    },
    'sample2': {
        'cd': (0, 2500),
        'cu': (0, 2500),
    }
}
