//- require('offline-plugin/runtime').install();  // offline service-worker plugin


// ------------------------------------- Libs -------------------------------------
import 'jquery'; window.$ = $; window.jQuery = jQuery;
import 'lodash'; window._ = _;
import 'vue'; import Vue from 'vue/dist/vue.esm.js'; window.Vue = Vue;
import 'bootstrap';
import 'promise-polyfill/src/polyfill';

import('fullcalendar');
import 'bootstrap-datepicker/dist/js/bootstrap-datepicker.min'
import 'bootstrap-datepicker'
import 'bootstrap-grid';

// import 'waypoints/lib/jquery.waypoints.js';
// import 'waypoints'; import Waypoint from 'waypoints'; window.Waypoint = Waypoint;

import 'typeface-roboto-condensed';
import 'typeface-roboto';
// import 'material-design-icons';
import '@fortawesome/fontawesome';
import '@fortawesome/fontawesome-free-brands';


// ---------------------------------- Modules -------------------------------------
// import '../scss/index.scss';

import './feedback';
import './header';
import './vue-env';
import './formula'

import './common';
