#include "CustomKnob.h"

CustomKnob::CustomKnob(const juce::String& knobID, NeuralPluginAudioProcessor& p)
    : knobComponentID(knobID),audioProcessor(p) {
	setSize(20, 50);
	knob.setComponentID(knobID);
	// Create and configure knobs with labels
	addAndMakeVisible(knob);
	knob.setRange(0, 1);
	knob.setSliderStyle(juce::Slider::RotaryHorizontalDrag);
    knob.setLookAndFeel(&otherLookAndFeel);
}

void CustomKnob::paint(juce::Graphics& g)
{
    knob.addListener(this);
}

void CustomKnob::resized()
{
	knob.setBounds(getLocalBounds()); 

}

void CustomKnob::sliderValueChanged(juce::Slider* slider)
{
    if (slider->getComponentID() == knobComponentID)
    {
        if (knobComponentID == "volume")
        {
            audioProcessor.setValueKnob1(float(knob.getValue()));
        }

        if (knobComponentID == "tone")
        {
            audioProcessor.setValueKnob2(float(knob.getValue()));
        }

        if (knobComponentID == "distortion")
        {
            audioProcessor.setValueKnob3(float(knob.getValue()));
        }

    }

}

void OtherLookAndFeel::drawRotarySlider(juce::Graphics& g, int x, int y, int width, int height, float sliderPos, float rotaryStartAngle, float rotaryEndAngle, juce::Slider& slider)
{

        float diameter = fmin(width, height) * 0.8;
        float radius = diameter / 2;
        float centerX = x + width / static_cast<float>(2);
        float centerY = y + height / static_cast<float>(2);
        float rx = centerX - radius;
        float ry = centerY - radius;
        float angle = rotaryStartAngle + (sliderPos * (rotaryEndAngle - rotaryStartAngle));

        juce::Rectangle<float> dialArea(rx, ry, diameter, diameter);
        juce::Rectangle<int> dialArea1(rx, ry, diameter, diameter);
        juce::Path dialTick;
        juce::Path dialTickContour;
        juce::Path ellipse;
        juce::Path arc;
        juce::DropShadow shadow;

        g.setColour(juce::Colours::transparentBlack);

        arc.addArc(rx, ry + 8, diameter, diameter, juce::float_Pi * 0.5, juce::float_Pi * 1.5, true);
        g.fillPath(arc);


        shadow.drawForPath(g, arc);

        g.setColour(juce::Colours::dimgrey);
        g.fillEllipse(dialArea);

        g.setColour(juce::Colours::darkslategrey);
        ellipse.addEllipse((centerX - radius * 0.8), (centerY - radius * 0.8), diameter * 0.8, diameter * 0.8);
        g.fillPath(ellipse);


        g.setColour(juce::Colours::black);
        g.drawEllipse((centerX - radius * 0.8), (centerY - radius * 0.8), diameter * 0.8, diameter * 0.8, 2.5f);

        shadow.colour = juce::Colours::grey;
        shadow.drawForPath(g, ellipse);

        g.setColour(juce::Colours::aqua);
        dialTick.addRectangle(0, -radius, 6.0f, radius * 0.5);
        g.fillPath(dialTick, juce::AffineTransform::rotation(angle).translated(centerX, centerY));
        shadow.radius = 30;
        shadow.colour = juce::Colours::aqua;
        shadow.drawForPath(g, dialTick);


        g.setColour(juce::Colours::black);
        dialTickContour.addRectangle(0, -radius, 6.0f, radius * 0.5);
        g.strokePath(dialTickContour, juce::PathStrokeType(2.0, juce::PathStrokeType::JointStyle::beveled),
            juce::AffineTransform::rotation(angle).translated(centerX, centerY));



        g.setColour(juce::Colours::black);
        g.drawEllipse(rx, ry, diameter, diameter, 2.5f);

}


