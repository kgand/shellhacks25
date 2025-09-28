"""
Routine Management Agent

This agent specializes in helping individuals with Alzheimer's disease
manage their daily routines, medications, appointments, and activities.
"""

import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta, time
import asyncio

class RoutineManagementAgent:
    """
    Specialized agent for daily routine management and schedule assistance.
    Provides medication reminders, appointment scheduling, and activity guidance.
    """
    
    def __init__(self, user_id: str):
        """
        Initialize the routine management agent.
        
        Args:
            user_id: Unique identifier for the user
        """
        self.user_id = user_id
        self.agent_id = "routine_management"
        
        # Routine database structure
        self.routine_database = {
            "daily_schedule": [],
            "medications": [],
            "appointments": [],
            "activities": [],
            "meal_times": [],
            "bedtime_routine": []
        }
        
        # Reminder system
        self.active_reminders = []
        self.reminder_templates = {
            "medication": "Time for your {medication_name}",
            "appointment": "You have an appointment with {doctor_name} at {time}",
            "meal": "Time for {meal_type}",
            "activity": "Time for your {activity_name}"
        }
        
        # Initialize with default routines
        self._initialize_default_routines()
    
    async def process_request(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process routine-related requests and provide appropriate assistance.
        
        Args:
            input_data: User input data
            context: Current session context
            
        Returns:
            Response from the routine management agent
        """
        try:
            content = input_data.get("content", "").lower()
            input_type = input_data.get("type", "text")
            
            # Determine the type of routine assistance needed
            if "medicine" in content or "medication" in content or "pill" in content:
                return await self._handle_medication_request(content, context)
            elif "appointment" in content or "doctor" in content or "schedule" in content:
                return await self._handle_appointment_request(content, context)
            elif "time" in content or "what time" in content or "when" in content:
                return await self._handle_time_request(content, context)
            elif "meal" in content or "eat" in content or "food" in content:
                return await self._handle_meal_request(content, context)
            elif "activity" in content or "exercise" in content or "walk" in content:
                return await self._handle_activity_request(content, context)
            elif "routine" in content or "schedule" in content or "today" in content:
                return await self._handle_daily_routine_request(content, context)
            else:
                return await self._handle_general_routine_support(content, context)
                
        except Exception as e:
            return {
                "agent": self.agent_id,
                "error": True,
                "message": f"Error in routine management: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _handle_medication_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle medication-related requests."""
        current_time = datetime.now()
        
        # Check if it's time for medication
        due_medications = self._get_due_medications(current_time)
        
        if due_medications:
            response_text = self._format_medication_reminder(due_medications)
            reminder_type = "medication_due"
        else:
            next_medication = self._get_next_medication(current_time)
            response_text = self._format_next_medication_info(next_medication)
            reminder_type = "medication_info"
        
        return {
            "agent": self.agent_id,
            "type": "medication",
            "content": response_text,
            "reminder_type": reminder_type,
            "medications_due": len(due_medications),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_appointment_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle appointment-related requests."""
        current_time = datetime.now()
        
        # Get today's appointments
        today_appointments = self._get_today_appointments(current_time)
        
        if today_appointments:
            response_text = self._format_appointment_reminder(today_appointments)
        else:
            upcoming_appointments = self._get_upcoming_appointments(current_time)
            response_text = self._format_upcoming_appointments(upcoming_appointments)
        
        return {
            "agent": self.agent_id,
            "type": "appointment",
            "content": response_text,
            "appointments_today": len(today_appointments),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_time_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle time-related requests."""
        current_time = datetime.now()
        
        # Determine what time information is needed
        if "what time" in content:
            response_text = f"It's currently {current_time.strftime('%I:%M %p')} on {current_time.strftime('%A, %B %d')}"
        elif "next" in content:
            next_activity = self._get_next_scheduled_activity(current_time)
            response_text = self._format_next_activity_info(next_activity)
        else:
            response_text = self._format_current_time_info(current_time)
        
        return {
            "agent": self.agent_id,
            "type": "time_info",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_meal_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle meal-related requests."""
        current_time = datetime.now()
        
        # Determine meal time
        meal_type = self._determine_meal_type(current_time)
        next_meal = self._get_next_meal_time(current_time)
        
        response_text = self._format_meal_reminder(meal_type, next_meal)
        
        return {
            "agent": self.agent_id,
            "type": "meal",
            "content": response_text,
            "meal_type": meal_type,
            "next_meal": next_meal,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_activity_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle activity-related requests."""
        current_time = datetime.now()
        
        # Get scheduled activities
        scheduled_activities = self._get_scheduled_activities(current_time)
        
        if scheduled_activities:
            response_text = self._format_activity_reminder(scheduled_activities)
        else:
            suggested_activities = self._get_suggested_activities()
            response_text = self._format_activity_suggestions(suggested_activities)
        
        return {
            "agent": self.agent_id,
            "type": "activity",
            "content": response_text,
            "activities_scheduled": len(scheduled_activities),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_daily_routine_request(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle daily routine requests."""
        current_time = datetime.now()
        
        # Get today's complete schedule
        daily_schedule = self._get_daily_schedule(current_time)
        
        response_text = self._format_daily_schedule(daily_schedule)
        
        return {
            "agent": self.agent_id,
            "type": "daily_routine",
            "content": response_text,
            "schedule_items": len(daily_schedule),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_general_routine_support(self, content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general routine support requests."""
        response_text = self._provide_general_routine_support(content)
        
        return {
            "agent": self.agent_id,
            "type": "general_support",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_due_medications(self, current_time: datetime) -> List[Dict[str, Any]]:
        """Get medications that are due now."""
        due_medications = []
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        for medication in self.routine_database["medications"]:
            if medication.get("active", True):
                scheduled_time = medication.get("scheduled_time")
                if scheduled_time:
                    med_hour, med_minute = map(int, scheduled_time.split(":"))
                    # Check if it's within 30 minutes of scheduled time
                    if (current_hour == med_hour and abs(current_minute - med_minute) <= 30):
                        due_medications.append(medication)
        
        return due_medications
    
    def _get_next_medication(self, current_time: datetime) -> Optional[Dict[str, Any]]:
        """Get the next scheduled medication."""
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        next_medication = None
        next_time = None
        
        for medication in self.routine_database["medications"]:
            if medication.get("active", True):
                scheduled_time = medication.get("scheduled_time")
                if scheduled_time:
                    med_hour, med_minute = map(int, scheduled_time.split(":"))
                    med_time = med_hour * 60 + med_minute
                    current_time_minutes = current_hour * 60 + current_minute
                    
                    if med_time > current_time_minutes:
                        if next_time is None or med_time < next_time:
                            next_medication = medication
                            next_time = med_time
        
        return next_medication
    
    def _get_today_appointments(self, current_time: datetime) -> List[Dict[str, Any]]:
        """Get today's appointments."""
        today_appointments = []
        today_date = current_time.date()
        
        for appointment in self.routine_database["appointments"]:
            appointment_date = appointment.get("date")
            if appointment_date and appointment_date == today_date.isoformat():
                today_appointments.append(appointment)
        
        return today_appointments
    
    def _get_upcoming_appointments(self, current_time: datetime) -> List[Dict[str, Any]]:
        """Get upcoming appointments."""
        upcoming_appointments = []
        current_date = current_time.date()
        
        for appointment in self.routine_database["appointments"]:
            appointment_date = appointment.get("date")
            if appointment_date:
                appt_date = datetime.fromisoformat(appointment_date).date()
                if appt_date >= current_date:
                    upcoming_appointments.append(appointment)
        
        # Sort by date
        upcoming_appointments.sort(key=lambda x: x.get("date", ""))
        return upcoming_appointments[:3]  # Return next 3 appointments
    
    def _get_next_scheduled_activity(self, current_time: datetime) -> Optional[Dict[str, Any]]:
        """Get the next scheduled activity."""
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        next_activity = None
        next_time = None
        
        for activity in self.routine_database["activities"]:
            scheduled_time = activity.get("scheduled_time")
            if scheduled_time:
                act_hour, act_minute = map(int, scheduled_time.split(":"))
                act_time = act_hour * 60 + act_minute
                current_time_minutes = current_hour * 60 + current_minute
                
                if act_time > current_time_minutes:
                    if next_time is None or act_time < next_time:
                        next_activity = activity
                        next_time = act_time
        
        return next_activity
    
    def _determine_meal_type(self, current_time: datetime) -> str:
        """Determine what meal it should be based on time."""
        current_hour = current_time.hour
        
        if 6 <= current_hour < 11:
            return "breakfast"
        elif 11 <= current_hour < 15:
            return "lunch"
        elif 15 <= current_hour < 19:
            return "dinner"
        else:
            return "snack"
    
    def _get_next_meal_time(self, current_time: datetime) -> Optional[str]:
        """Get the next meal time."""
        current_hour = current_time.hour
        
        if current_hour < 8:
            return "8:00 AM - Breakfast"
        elif current_hour < 12:
            return "12:00 PM - Lunch"
        elif current_hour < 18:
            return "6:00 PM - Dinner"
        else:
            return "8:00 AM tomorrow - Breakfast"
    
    def _get_scheduled_activities(self, current_time: datetime) -> List[Dict[str, Any]]:
        """Get activities scheduled for now."""
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        scheduled_activities = []
        
        for activity in self.routine_database["activities"]:
            scheduled_time = activity.get("scheduled_time")
            if scheduled_time:
                act_hour, act_minute = map(int, scheduled_time.split(":"))
                if (act_hour == current_hour and abs(act_minute - current_minute) <= 30):
                    scheduled_activities.append(activity)
        
        return scheduled_activities
    
    def _get_suggested_activities(self) -> List[Dict[str, Any]]:
        """Get suggested activities for the current time."""
        current_time = datetime.now()
        current_hour = current_time.hour
        
        if 6 <= current_hour < 9:
            return [
                {"name": "Morning walk", "description": "A gentle walk around the neighborhood"},
                {"name": "Breakfast", "description": "Enjoy a healthy breakfast"},
                {"name": "Newspaper reading", "description": "Read the morning paper"}
            ]
        elif 9 <= current_hour < 12:
            return [
                {"name": "Gardening", "description": "Tend to your garden or plants"},
                {"name": "Crafts", "description": "Work on a craft project"},
                {"name": "Music", "description": "Listen to your favorite music"}
            ]
        elif 12 <= current_hour < 15:
            return [
                {"name": "Lunch", "description": "Have a nutritious lunch"},
                {"name": "Rest", "description": "Take a short nap or rest"},
                {"name": "Reading", "description": "Read a book or magazine"}
            ]
        else:
            return [
                {"name": "Evening walk", "description": "A gentle evening stroll"},
                {"name": "Dinner", "description": "Enjoy dinner"},
                {"name": "Relaxation", "description": "Relax and unwind"}
            ]
    
    def _get_daily_schedule(self, current_time: datetime) -> List[Dict[str, Any]]:
        """Get today's complete schedule."""
        daily_schedule = []
        
        # Add medications
        for medication in self.routine_database["medications"]:
            if medication.get("active", True):
                daily_schedule.append({
                    "time": medication.get("scheduled_time", ""),
                    "activity": f"Take {medication.get('name', 'medication')}",
                    "type": "medication"
                })
        
        # Add appointments
        today_appointments = self._get_today_appointments(current_time)
        for appointment in today_appointments:
            daily_schedule.append({
                "time": appointment.get("time", ""),
                "activity": f"Appointment with {appointment.get('doctor_name', 'doctor')}",
                "type": "appointment"
            })
        
        # Add activities
        for activity in self.routine_database["activities"]:
            if activity.get("active", True):
                daily_schedule.append({
                    "time": activity.get("scheduled_time", ""),
                    "activity": activity.get("name", "Activity"),
                    "type": "activity"
                })
        
        # Sort by time
        daily_schedule.sort(key=lambda x: x.get("time", ""))
        return daily_schedule
    
    def _format_medication_reminder(self, medications: List[Dict[str, Any]]) -> str:
        """Format medication reminder message."""
        if not medications:
            return "No medications are due right now."
        
        response = "It's time for your medication:\n\n"
        for med in medications:
            response += f"• {med.get('name', 'Medication')} - {med.get('dosage', '1 pill')}\n"
            if med.get('instructions'):
                response += f"  Instructions: {med['instructions']}\n"
        
        response += "\nPlease take your medication as directed."
        return response
    
    def _format_next_medication_info(self, medication: Optional[Dict[str, Any]]) -> str:
        """Format next medication information."""
        if not medication:
            return "No more medications scheduled for today."
        
        return f"Your next medication is {medication.get('name', 'medication')} at {medication.get('scheduled_time', 'unknown time')}."
    
    def _format_appointment_reminder(self, appointments: List[Dict[str, Any]]) -> str:
        """Format appointment reminder message."""
        if not appointments:
            return "No appointments scheduled for today."
        
        response = "You have appointments today:\n\n"
        for appointment in appointments:
            response += f"• {appointment.get('time', 'Unknown time')} - {appointment.get('doctor_name', 'Doctor')}\n"
            if appointment.get('location'):
                response += f"  Location: {appointment['location']}\n"
            if appointment.get('notes'):
                response += f"  Notes: {appointment['notes']}\n"
        
        return response
    
    def _format_upcoming_appointments(self, appointments: List[Dict[str, Any]]) -> str:
        """Format upcoming appointments message."""
        if not appointments:
            return "No upcoming appointments scheduled."
        
        response = "Your upcoming appointments:\n\n"
        for appointment in appointments:
            appt_date = datetime.fromisoformat(appointment.get('date', '')).strftime('%A, %B %d')
            response += f"• {appt_date} at {appointment.get('time', 'Unknown time')} - {appointment.get('doctor_name', 'Doctor')}\n"
        
        return response
    
    def _format_next_activity_info(self, activity: Optional[Dict[str, Any]]) -> str:
        """Format next activity information."""
        if not activity:
            return "No activities scheduled for today."
        
        return f"Your next activity is {activity.get('name', 'activity')} at {activity.get('scheduled_time', 'unknown time')}."
    
    def _format_current_time_info(self, current_time: datetime) -> str:
        """Format current time information."""
        return f"It's {current_time.strftime('%I:%M %p')} on {current_time.strftime('%A, %B %d, %Y')}."
    
    def _format_meal_reminder(self, meal_type: str, next_meal: Optional[str]) -> str:
        """Format meal reminder message."""
        if meal_type in ["breakfast", "lunch", "dinner"]:
            return f"It's time for {meal_type}. {next_meal if next_meal else 'Enjoy your meal!'}"
        else:
            return f"You might want a snack. {next_meal if next_meal else 'Take care of yourself!'}"
    
    def _format_activity_reminder(self, activities: List[Dict[str, Any]]) -> str:
        """Format activity reminder message."""
        if not activities:
            return "No activities scheduled right now."
        
        response = "It's time for your activities:\n\n"
        for activity in activities:
            response += f"• {activity.get('name', 'Activity')}\n"
            if activity.get('description'):
                response += f"  {activity['description']}\n"
        
        return response
    
    def _format_activity_suggestions(self, activities: List[Dict[str, Any]]) -> str:
        """Format activity suggestions message."""
        if not activities:
            return "No activities suggested at this time."
        
        response = "Here are some activities you might enjoy:\n\n"
        for activity in activities:
            response += f"• {activity.get('name', 'Activity')} - {activity.get('description', '')}\n"
        
        return response
    
    def _format_daily_schedule(self, schedule: List[Dict[str, Any]]) -> str:
        """Format daily schedule message."""
        if not schedule:
            return "No schedule items for today."
        
        response = "Here's your schedule for today:\n\n"
        for item in schedule:
            response += f"• {item.get('time', 'Unknown time')} - {item.get('activity', 'Activity')}\n"
        
        return response
    
    def _provide_general_routine_support(self, content: str) -> str:
        """Provide general routine support."""
        responses = [
            "I'm here to help you with your daily routine. What would you like to know?",
            "Let me help you stay on track with your schedule. What do you need?",
            "I can help you remember your medications, appointments, and activities. What would you like to check?",
            "Your routine is important for your wellbeing. How can I help you today?"
        ]
        
        # Simple response selection based on content
        if "help" in content:
            return responses[0]
        elif "schedule" in content:
            return responses[1]
        elif "remember" in content:
            return responses[2]
        else:
            return responses[3]
    
    def _initialize_default_routines(self):
        """Initialize default routines and schedules."""
        # Add some default medications
        self.routine_database["medications"] = [
            {
                "id": "med_001",
                "name": "Morning Vitamin",
                "dosage": "1 tablet",
                "scheduled_time": "08:00",
                "instructions": "Take with breakfast",
                "active": True
            },
            {
                "id": "med_002", 
                "name": "Evening Medication",
                "dosage": "1 capsule",
                "scheduled_time": "20:00",
                "instructions": "Take with dinner",
                "active": True
            }
        ]
        
        # Add some default activities
        self.routine_database["activities"] = [
            {
                "id": "act_001",
                "name": "Morning Walk",
                "scheduled_time": "09:00",
                "description": "A gentle 15-minute walk",
                "active": True
            },
            {
                "id": "act_002",
                "name": "Reading Time",
                "scheduled_time": "14:00", 
                "description": "Read for 30 minutes",
                "active": True
            }
        ]
    
    def add_medication(self, medication_data: Dict[str, Any]):
        """Add a new medication to the routine."""
        medication_data["id"] = str(uuid.uuid4())
        medication_data["active"] = True
        self.routine_database["medications"].append(medication_data)
    
    def add_appointment(self, appointment_data: Dict[str, Any]):
        """Add a new appointment."""
        appointment_data["id"] = str(uuid.uuid4())
        self.routine_database["appointments"].append(appointment_data)
    
    def add_activity(self, activity_data: Dict[str, Any]):
        """Add a new activity to the routine."""
        activity_data["id"] = str(uuid.uuid4())
        activity_data["active"] = True
        self.routine_database["activities"].append(activity_data)
