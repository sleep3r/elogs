require('offline-plugin/runtime').install();

import 'bootstrap'; // for usage directly on pages
import 'fullcalendar';
import 'jquery-confirm';
// import 'font-awesome-webpack';

require('../scss/index.scss');

import './shift'
import './cell'
import './datepicker-init'
import './feedback'
import './form-table'
import './form-update'
import './header'
import './menu'
import './vue-env'

// Независимые штуки
import './common'
import './journal-panel'
import './datepicker'
import './user-menu'
