#pragma once

//Qt includes
#include <QAbstractSlider>
#include <QLabel>
#include <QStyle>
#include <QStyleFactory>
#include <QStyleOptionSlider>





//class MyIntervalSliderHandle;


//==================================================================================================
//					MyIntervalSliderOptions
//==================================================================================================

class MyIntervalSliderOptions
{
	QStyleOptionSlider commonOptions;
public:
	int lowerValue, lowerPosition;
	int upperValue, upperPosition;
	//QStyleOptionSlider lowerHandleOptions, upperHandleOptions;
	//QStyleOptionSlider grooveOptions;
public:
	MyIntervalSliderOptions(const QStyleOptionSlider& opt = QStyleOptionSlider());
	MyIntervalSliderOptions(int min, int max, QWidget *init = nullptr);
	void setCommonOptions(QStyleOptionSlider val);
	QStyleOptionSlider getCommonOptions() const;
	QStyleOptionSlider getLowerHandleOptions() const;
	QStyleOptionSlider getUpperHandleOptions() const;
	QStyleOptionSlider getGrooveOptions() const;
	bool setLowerValue(int value);
	bool setUpperValue(int value);
	void update(QWidget *parent);
};


//==================================================================================================
//					MyIntervalSlider 
//==================================================================================================

class MyIntervalSlider : public QAbstractSlider
{
	Q_OBJECT
private:
	const int leftIndent = 7, rightIndent = 7;
	int range, actualRange;
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
	int upperValue();
	int lowerValue();

	/** Convenience functions for setting the value of the handles */
	void setUpperValue(int value);
	void setLowerValue(int value);

signals:
	void upperValueChanged();
	void lowerValueChanged(int);
};


