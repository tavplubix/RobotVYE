
//Project includes
#include "MyIntervalSlider.h"

//Qt includes
#include <QMouseEvent>
#include <QMimeData>
#include <QDrag>
#include <QWidgetAction>
#include <QApplication>
#include <QPixmap>
#include <QCursor>
#include <QGuiApplication>
#include <QDir>
#include <QProxyStyle>
#include <QStylePainter>


//==================================================================================================
//					MyIntervalSliderOptions
//==================================================================================================

MyIntervalSliderOptions::MyIntervalSliderOptions(QAbstractSlider *slider) 
	: slider(slider)
{
	m_lowerPosition = m_lowerValue = slider->minimum();
	m_upperPosition = m_upperValue = slider->maximum();
}

QStyleOptionSlider MyIntervalSliderOptions::copyOptions() const
{
	QStyleOptionSlider opt;
	opt.initFrom(slider);
	opt.maximum = slider->maximum();
	opt.minimum = slider->minimum();
	opt.orientation = slider->orientation();
	opt.pageStep = slider->pageStep();
	opt.singleStep = slider->singleStep();
	return opt;
}

QStyleOptionSlider MyIntervalSliderOptions::getCommonOptions() const
{
	return copyOptions();
}
QStyleOptionSlider MyIntervalSliderOptions::getLowerHandleOptions() const
{
	QStyleOptionSlider opt = copyOptions();
	opt.subControls = QStyle::SC_SliderHandle;
	opt.sliderPosition = m_lowerPosition;
	opt.sliderValue = m_lowerValue;
	return opt;
}
QStyleOptionSlider MyIntervalSliderOptions::getUpperHandleOptions() const
{
	QStyleOptionSlider opt = copyOptions();
	opt.subControls = QStyle::SC_SliderHandle;
	opt.sliderPosition = m_upperPosition;
	opt.sliderValue = m_upperValue;
	return opt;
}
QStyleOptionSlider MyIntervalSliderOptions::getGrooveOptions() const
{
	QStyleOptionSlider opt = copyOptions();
	opt.subControls = QStyle::SC_SliderGroove | QStyle::SC_SliderTickmarks;
	return opt;
}
bool MyIntervalSliderOptions::setLowerValue(int value)		
{
	if (value >= m_upperValue) return false;
	m_lowerValue = value;
	m_lowerPosition = value;
	return true;
}
bool MyIntervalSliderOptions::setUpperValue(int value)		
{
	if (value <= m_lowerValue) return false;
	m_upperValue = value;
	m_upperPosition = value;
	return true;
}


//==================================================================================================
//					MyIntervalSlider Implementation
//==================================================================================================

MyIntervalSlider::MyIntervalSlider(QWidget *parent)
	: QAbstractSlider(parent), 
	activeSubControl(None)
{

	//HARDCODED
	QStringList keys = QStyleFactory::keys();
	style = QStyleFactory::create("Fusion");
	//style = qApp->style();
	setStyle(style);
	options = new MyIntervalSliderOptions(this);

	//styling
	setAcceptDrops(true);
}

MyIntervalSlider::~MyIntervalSlider()
{
	delete options;
	delete style;
}

void MyIntervalSlider::paintEvent(QPaintEvent *)
{
	QStylePainter painter(this);
	//options->update(this);
	//draw slider's subelements
	painter.drawComplexControl(QStyle::CC_Slider, options->getGrooveOptions());
	painter.drawComplexControl(QStyle::CC_Slider, options->getLowerHandleOptions());
	painter.drawComplexControl(QStyle::CC_Slider, options->getUpperHandleOptions());
}



MyIntervalSlider::SubControl MyIntervalSlider::subcontrolOnPosition(const QPoint& position)
{
	QStyle::SubControl element;
	/*element = style->hitTestComplexControl(QStyle::CC_Slider, &options->getLowerHandleOptions(), position);
	if (element == ) return LowerHandle;
	element = style->hitTestComplexControl(QStyle::CC_Slider, &options->getUpperHandleOptions(), position);
	if (element) return UpperHandle;
	element = style->hitTestComplexControl(QStyle::CC_Slider, &options->getGrooveOptions(), position);
	if (element) return Groove;*/
	QRect rect;
	rect = style->subControlRect(QStyle::CC_Slider, &options->getUpperHandleOptions(), QStyle::SC_SliderHandle);
	if (rect.contains(position)) return UpperHandle;
	rect = style->subControlRect(QStyle::CC_Slider, &options->getLowerHandleOptions(), QStyle::SC_SliderHandle);
	if (rect.contains(position)) return LowerHandle;
	rect = style->subControlRect(QStyle::CC_Slider, &options->getGrooveOptions(), QStyle::SC_SliderGroove);
	if (rect.contains(position)) return Groove;
	return None;
}


void MyIntervalSlider::mousePressEvent(QMouseEvent *event)
{
	QPoint pos = event->pos();
	if (event->button() == Qt::LeftButton) {
		activeSubControl = subcontrolOnPosition(pos);
		clearFocus();
	}
	event->accept();
}

void MyIntervalSlider::mouseMoveEvent(QMouseEvent *event)
{
	QPoint pos = event->pos();
	int min = options->getCommonOptions().minimum;
	int max = options->getCommonOptions().maximum;
	double pixelsPerOne = width() / double(maximum() - minimum());
	int ones = pos.x() / pixelsPerOne;
	int newValue = min + ones;
	if (newValue < min) newValue = min;
	if (newValue > max) newValue = max;

	if (activeSubControl == LowerHandle) {
		options->setLowerValue(newValue);
		emit lowerValueChanged(options->lowerValue());
	}
	if (activeSubControl == UpperHandle) {
		options->setUpperValue(newValue);
		emit upperValueChanged(options->upperValue());
	}
	emit valueChanged(newValue);
	event->accept();
	update();
}

void MyIntervalSlider::mouseReleaseEvent(QMouseEvent *mouseEvent)
{
	if (mouseEvent->button() == Qt::LeftButton) {
		activeSubControl = None;
	}
	mouseEvent->accept();
}

void MyIntervalSlider::setUpperValue(int value)
{
	int oldValue = upperValue();
	options->setUpperValue(value);
	if (value != oldValue) {
		emit upperValueChanged(upperValue());
		emit valueChanged(upperValue());
	}
}
void MyIntervalSlider::setLowerValue(int value)
{
	int oldValue = lowerValue();
	options->setLowerValue(value);
	if (value != oldValue) {
		emit lowerValueChanged(lowerValue());
		emit valueChanged(lowerValue());
	}
}







