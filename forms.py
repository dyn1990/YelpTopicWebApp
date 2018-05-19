from flask_wtf import Form 
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


# class SelectForm(Form):    
# 	choice_list = [("extreme", "Extreme"), ("japanese", "Japanese")]
# 	topic = SelectField('Please select a topic', choices=choice_list)
# 	rests = StringField('Restaurant', validators=[DataRequired("Please enter a topic.")])
	# submit = SubmitField("Display")

# from wtforms import Form, StringField, SelectField
 
class TopicSearchForm(Form):
    choices = [("general", "General"),
    ("menu", "Menu"),
    ("service", "Service"),
    ("location", "Location"),
    ("american", "American"),
    ("japanese", "Japanese"),
    ("mexico", "Mexico"),
    ("canadian", "Canadian"),
    ("italian", "Italian"),
    ("bar", "Bar"),
    ("breakfast", "Breakfast"),
    ("lunch", "Lunch"),
    ("dinner", "Dinner"),
    ("buffet", "Buffet"),
    ("burger", "Burger"),
    ("steal", "Steak"),
    ("lamb", "Lamb"),
    ("sandwich", "Sandwich"),
    ("refreshment", "Refreshment")]

    choices_star = [("5", "5"),
    ("4", "4"),
    ("3", "3"),
    ("2", "2"),
    ("1", "1"),]
    select = SelectField('Search for topic:', choices=choices)
    star = SelectField('Select stars:', choices=choices_star)
    search = StringField('Please enter a restaurant name:',
    	render_kw={"placeholder": "Bacchanal Buffet"})
    begin_date = StringField('Please enter the start date:',
        render_kw={"placeholder": "2017-05-01"})
    end_date = StringField('Please enter the end date:',
        render_kw={"placeholder": "2017-10-01"})

class reviewPredForm(Form):
	text_input = TextAreaField('Please Write Your Review: ', 
		render_kw={"rows":6, "cols":50, 
		"placeholder": "I like the food at Bacchanal Buffet!"})