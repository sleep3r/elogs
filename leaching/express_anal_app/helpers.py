

def dump(rows):
    for r in rows:
        print(r.time.hour,r.ph,r.point, r.sink)



def denserData():
    context = {
        'rows': [
            {
            'time': 10,
            'denser': [{
                'upper': {
                    'ph': 0.16,
                    'cu': 0.25,
                    'fe': 0.34,
                    'liqSol': 0.43,
                },
                'lower': {
                    'ph': 0.52,
                    'liqSol': 0.61,
                }
            },
            {
                    'upper': {
                        'ph': 0.16,
                        'cu': 0.25,
                        'fe': 0.34,
                        'liqSol': 0.43,
                    },
                    'lower': {
                        'ph': 0.52,
                        'liqSol': 0.61,
                    }
                },
            {
                    'upper': {
                        'ph': 0.36,
                        'cu': 0.75,
                        'fe': 0.14,
                        'liqSol': 0.93,
                    },
                    'lower': {
                        'ph': 0.55,
                        'liqSol': 0.21,
                    }
            }],
        },
            {
            'time': 12,
            'denser': [{
                'upper': {
                    'ph': 0.16,
                    'cu': 0.25,
                    'fe': 0.34,
                    'liqSol': 0.43,
                },
                'lower': {
                    'ph': 0.52,
                    'liqSol': 0.61,
                }
            },
            {
                    'upper': {
                        'ph': 0.16,
                        'cu': 0.25,
                        'fe': 0.34,
                        'liqSol': 0.43,
                    },
                    'lower': {
                        'ph': 0.52,
                        'liqSol': 0.61,
                    }
                },
            {
                    'upper': {
                        'ph': 0.36,
                        'cu': 0.75,
                        'fe': 0.14,
                        'liqSol': 0.93,
                    },
                    'lower': {
                        'ph': 0.55,
                        'liqSol': 0.21,
                    }
            }],
        },
            {
            'time': 16,
            'denser': [{
                'upper': {
                    'ph': 0.16,
                    'cu': 0.25,
                    'fe': 0.34,
                    'liqSol': 0.43,
                },
                'lower': {
                    'ph': 0.52,
                    'liqSol': 0.61,
                }
            },
            {
                    'upper': {
                        'ph': 0.16,
                        'cu': 0.25,
                        'fe': 0.34,
                        'liqSol': 0.43,
                    },
                    'lower': {
                        'ph': 0.52,
                        'liqSol': 0.61,
                    }
                },
            {
                    'upper': {
                        'ph': 0.36,
                        'cu': 0.75,
                        'fe': 0.14,
                        'liqSol': 0.93,
                    },
                    'lower': {
                        'ph': 0.55,
                        'liqSol': 0.21,
                    }
            }],
        },
            {
                    'time': 18,
                    'denser': [{
                        'upper': {
                            'ph': 0.16,
                            'cu': 0.25,
                            'fe': 0.34,
                            'liqSol': 0.43,
                        },
                        'lower': {
                            'ph': 0.52,
                            'liqSol': 0.61,
                        }
                    },
                        {
                            'upper': {
                                'ph': 0.16,
                                'cu': 0.25,
                                'fe': 0.34,
                                'liqSol': 0.43,
                            },
                            'lower': {
                                'ph': 0.52,
                                'liqSol': 0.61,
                            }
                        },
                        {
                            'upper': {
                                'ph': 0.36,
                                'cu': 0.75,
                                'fe': 0.14,
                                'liqSol': 0.93,
                            },
                            'lower': {
                                'ph': 0.55,
                                'liqSol': 0.21,
                            }
                        }],
                },
            {
                'time': 20,
                'denser': [{
                    'upper': {
                        'ph': 0.16,
                        'cu': 0.25,
                        'fe': 0.34,
                        'liqSol': 0.43,
                    },
                    'lower': {
                        'ph': 0.52,
                        'liqSol': 0.61,
                    }
                },
                    {
                        'upper': {
                            'ph': 0.16,
                            'cu': 0.25,
                            'fe': 0.34,
                            'liqSol': 0.43,
                        },
                        'lower': {
                            'ph': 0.52,
                            'liqSol': 0.61,
                        }
                    },
                    {
                        'upper': {
                            'ph': 0.36,
                            'cu': 0.75,
                            'fe': 0.14,
                            'liqSol': 0.93,
                        },
                        'lower': {
                            'ph': 0.55,
                            'liqSol': 0.21,
                        }
                    }],
            }
        ]
    }
    return context