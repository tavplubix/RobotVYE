#pragma once

//Qt includes
#include <QAbstractSlider>
#include <QLabel>
#include <QStyle>
#include <QStyleFactory>
#include <QStyleOptionSlider>


//==================================================================================================
//					MyIntervalSliderOptions
//==================================================================================================

class MyIntervalSliderOptions
{
	QAbstractSlider *slider;
	QStyleOptionSlider copyOptions() const;
	int m_lowerValue, m_lowerPosition;
	int m_upperValue, m_upperPosition;
public:
	MyIntervalSliderOptions(QAbstractSlider *slider);
	QStyleOptionSlider getCommonOptions() const;
	QStyleOptionSlider getLowerHandleOptions() const;
	QStyleOptionSlider getUpperHandleOptions() const;
	QStyleOptionSlider getGrooveOptions() const;
	bool setLowerValue(int value);
	bool setUpperValue(int value);
	int lowerValue() const { return m_lowerValue; };
	int upperValue() const { return m_upperValue; };
	int lowerPosition() const { return m_lowerPosition; };
	int upperPosition() const { return m_upperPosition; };
};


//==================================================================================================
//					MyIntervalSlider 
//==================================================================================================

class MyIntervalSlider : public QAbstractSlider
{
	Q_OBJECT
private:
	QStyle *style;
	MyIntervalSliderOptions *options;
	void paintEvent(QPaintEvent *) final;
	enum SubControl {
		None = 0, Groove = QStyle::SC_SliderGroove, LowerHandle = QStyle::SC_SliderHandle, Tickmarks = QStyle::SC_SliderTickmarks, UpperHandle = 0x08
	};
	SubControl subcontrolOnPosition(const QPoint& position);
	SubControl activeSubControl;
public:
	/** Constructor */
	MyIntervalSlider(QWidget *parent = 0);

	//The rule of 5:
	~MyIntervalSlider();
	MyIntervalSlider(const MyIntervalSlider&) = delete;
	MyIntervalSlider(const MyIntervalSlider&&) = delete;
	MyIntervalSlider& operator=(const MyIntervalSlider&) = delete;
	MyIntervalSlider& operator=(const MyIntervalSlider&&) = delete;

	/** Overridden mouse events */
	void mousePressEvent(QMouseEvent *event) final;
	void mouseMoveEvent(QMouseEvent *event) final;
	void mouseReleaseEvent(QMouseEvent *event) final;

	/** Returns the slider value for the handle */

	int lowerValue() const { return options->lowerValue(); };
	int upperValue() const { return options->upperValue(); };
	int lowerPosition() const { return options->lowerPosition(); };
	int upperPosition() const { return options->upperPosition(); };

	/** Convenience functions for setting the value of the handles */
	void setUpperValue(int value);
	void setLowerValue(int value);

signals:
	void upperValueChanged(int);
	void lowerValueChanged(int);
};


