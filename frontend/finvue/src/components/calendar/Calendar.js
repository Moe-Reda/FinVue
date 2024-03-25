import React from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import './Calendar.css'
import 'react-big-calendar/lib/css/react-big-calendar.css';


const localizer = momentLocalizer(moment);
const MyCalendar = ({ events }) => {
    return (
      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        defaultView="month"
        style={{ height: 500 , width: 1000}} 
      />
    );
  };
export default MyCalendar;
