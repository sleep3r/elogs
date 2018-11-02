<template>
    <div class="clock-picker-wrapper" v-if="isPickerShown" @click="closeClockPicker">
        <div class="clock-picker" v-if="isPickerShown">
            <div class="picker-content" :style="{left: `${coordX}px`, top: `${coordY}px`}">
                <div class="picker-content_header">

                </div>
                <div class="picker-content_body">
                    <div class="clock">
                        <div class="center-dot"></div>
                        <template v-if="!currentHour">
                            <div 
                                class="hour day" 
                                v-for="(item, index) in data.hours.day" 
                                :key="'hour_day_' + item" 
                                :style="{top: `calc( 50% + ${getTop(index, 'hours', 'day')}px)`, left: `calc( 50% + ${getLeft(index, 'hours', 'day')}px`}"
                                @click="currentHour = item"
                            >
                                {{item}}
                            </div>
                            <div 
                                class="hour night" 
                                v-for="(item, index) in data.hours.night" 
                                :key="'hour_night_' + item" 
                                :style="{top: `calc( 50% + ${getTop(index, 'hours', 'night')}px)`, left: `calc( 50% + ${getLeft(index, 'hours', 'night')}px`}"
                                @click="currentHour = item"
                            >
                                {{item}}
                            </div>
                        </template>
                        <div 
                            v-else
                            class="minute" 
                            v-for="(item, index) in data.minutes" 
                            :key="'minute_' + item" 
                            :style="{top: `calc( 50% + ${getTop(index, 'minutes')}px)`, left: `calc( 50% + ${getLeft(index, 'minutes')}px`}"
                            @click="currentMinute = item;setTime()"
                        >
                            {{item}}
                        </div>
                    </div>
                </div>
                <div class="picker-content_footer">
                    <button class="btn" @click="setTime(new Date())">Сейчас</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import $ from 'jquery'
    import EventBus from '../EventBus'

    export default {
        name: 'ClockPicker',
        props: {
            format: {
                default: 24
            },
            disabled: {
                default: false
            },
            target: {
                default: ''
            }
        },
        data () {
            return {
                isPickerShown: false,
                coordX: null,
                coordY: null,
                time: null,
                currentHour: null,
                currentMinute: null,
                dayRadius: 90,
                nightRadius: 60,
                data: {
                    format: '24',
                    hours: {
                        day: [
                            '00',
                            '13',
                            '14',
                            '15',
                            '16',
                            '17',
                            '18',
                            '19',
                            '20',
                            '21',
                            '22',
                            '23'
                        ],
                        night: [
                            '12',
                            '1',
                            '2',
                            '3',
                            '4',
                            '5',
                            '6',
                            '7',
                            '8',
                            '9',
                            '10',
                            '11'
                        ]
                    },
                    minutes: [
                        '00',
                        '05',
                        '10',
                        '15',
                        '20',
                        '25',
                        '30',
                        '35',
                        '40',
                        '45',
                        '50',
                        '55'
                    ]
                },
                tableName: null,
                fieldName: null,
                rowIndex: null,
                currentInput: null
            }
        },
        methods: {
            getTop (index, type, hoursType) {
                let deg = 360 * index / (type === 'hours' ? this.data.hours[hoursType].length : this.data.minutes.length) + 180
                let y = Math.sin((90 - deg) * Math.PI / 180) * (hoursType === 'night' ? this.nightRadius : this.dayRadius)
                return y
            },
            getLeft (index, type, hoursType) {
                let deg = 360 * index / (type === 'hours' ? this.data.hours[hoursType].length : this.data.minutes.length) + 180
                let x = Math.cos((90 - deg) * Math.PI / 180) * (hoursType === 'night' ? this.nightRadius : this.dayRadius)
                return -x
            },
            openClockPicker (x, y) {
                if (!this.disabled) {
                    $('body').css({'overflow': 'hidden'})
                    this.isPickerShown = true
                    this.coordX = x
                    this.coordY = y
                }
            },
            closeClockPicker (e) {
                if (e && e.target.className === 'clock-picker-wrapper' || !e) {
                    $('body').css({'overflow': ''})
                    this.time = null
                    this.currentHour = null
                    this.currentMinute = null
                    this.isPickerShown = false
                }
            },
            onHandleClick (options) {
                this.fieldName = options.fieldName
                this.rowIndex = options.rowIndex
                this.currentInput = options.event.srcElement
                let x = this.coordX;
                let y = this.coordY;
                    
                if (!this.isPickerShown) {
                    let $currentElement = $(options.event.srcElement)
                    let inputOffset = 6;
                    let popUpWidth = $('.picker-content').outerWidth() ? $('.picker-content').outerWidth() : 246;
                    let appWidth = $(window).outerWidth()
                    let popUpHeight = $('.picker-content').outerHeight() ? $('.picker-content').outerHeight() : 294;
                    let appHeight = $(window).outerHeight()
                    if (options.event.clientX + popUpWidth >= appWidth) {
                        x = options.event.clientX - options.event.offsetX - popUpWidth + $currentElement.outerWidth()
                    }
                    else {
                        x = options.event.clientX  - options.event.offsetX
                    }
                    if (options.event.clientY - options.event.offsetY + popUpHeight + $currentElement.outerHeight() >= appHeight) {
                        y = options.event.clientY - popUpHeight - options.event.offsetY - inputOffset
                    }
                    else {
                        y = options.event.clientY - options.event.offsetY + inputOffset + $currentElement.outerHeight()

                    }

                    this.openClockPicker(x, y)
                }
            },
            setTime (time) {
                if (time) {
                    this.time = ((time.getHours() < 10 && time.getHours() !== '00') ? "0" : "") + time.getHours() + ":" + 
                                    ((time.getMinutes() < 10) ? "0" : "") + time.getMinutes()
                }
                else {
                    this.time = (this.currentHour < 10 && this.currentHour !== '00' ? '0' : '') + this.currentHour + ':' + this.currentMinute
                }
                $(this.currentInput).val(this.time)
                setTimeout(() => this.closeClockPicker(), 0)
            }
        },
        mounted () {
            let self = this

            EventBus.$on('show-clock-picker', (props) => {
                self.onHandleClick(props)
            })
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
    .clock-picker-wrapper {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        z-index: 100;
    }
    .picker-content {
        position: absolute;
        padding: 12px;
        width: fit-content;
        background-color: #f8f8f8;
        box-shadow: 0px 0px 6px rgba(0,0,0,.2);
        z-index: 4;

        .picker-content_body {
            display: flex;
            justify-content: center;
        }

        .picker-content_body {
            .clock {
                position: relative;
                height: 220px;
                width: 220px;
                border: 1px solid #e0e0e0;
                border-radius: 50%;
                background-color: #fff;
            
                .center-dot {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    width: 4px;
                    height: 4px;
                    border-radius: 50%;
                    transform: translate(-50%, -50%);
                    background-color: #656565;
                }

                .hour, .minute {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    position: absolute;
                    width: 28px;
                    height: 28px;
                    transform: translate(-50%, -50%);
                    padding: 4px;
                    border-radius: 50%;
                    transition: 0.2s;
                    cursor: pointer;

                    &.night {
                        opacity: 0.8;
                    }
                }

                .hour:hover, .minute:hover {
                    background-color: #008BB9;
                    color: white;
                }
            }
        }

        .picker-content_footer {
            text-align: center;
            margin-top: 12px;
        }
    }
</style>
