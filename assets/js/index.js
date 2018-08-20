require('offline-plugin/runtime').install();  // offline service-worker plugin


// ------------------------------------- Libs -------------------------------------
import 'jquery'; window.$ = $; window.jQuery = jQuery;
import 'underscore'; window._ = _;
import 'vue'; import Vue from 'vue'; window.Vue = Vue;
import 'bootstrap'

import 'fullcalendar'
import 'bootstrap-datepicker'

import 'typeface-roboto-condensed'
import 'typeface-roboto'
import 'material-design-icons'
import '@fortawesome/fontawesome'
import '@fortawesome/fontawesome-free-brands'


// ---------------------------------- Modules -------------------------------------
import '../scss/index.scss';

import './shift'
import './cell'
import './datepicker-init'
import './feedback'
import './form-table'
import './form-update'
import './header'
import './menu'
import './vue-env'

import './common'
import './journal-panel'
import './user-menu'
