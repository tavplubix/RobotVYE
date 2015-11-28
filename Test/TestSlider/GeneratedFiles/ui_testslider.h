/********************************************************************************
** Form generated from reading UI file 'testslider.ui'
**
** Created by: Qt User Interface Compiler version 5.5.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_TESTSLIDER_H
#define UI_TESTSLIDER_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QSlider>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_TestSliderClass
{
public:
    QWidget *centralWidget;
    QWidget *verticalLayoutWidget;
    QVBoxLayout *verticalLayout;
    QLabel *lowerLabel;
    QLabel *upperLabel;
    QLabel *NativePosLabel;
    QLabel *posLabel;
    QSlider *horizontalSlider;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *TestSliderClass)
    {
        if (TestSliderClass->objectName().isEmpty())
            TestSliderClass->setObjectName(QStringLiteral("TestSliderClass"));
        TestSliderClass->resize(1103, 769);
        centralWidget = new QWidget(TestSliderClass);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        verticalLayoutWidget = new QWidget(centralWidget);
        verticalLayoutWidget->setObjectName(QStringLiteral("verticalLayoutWidget"));
        verticalLayoutWidget->setGeometry(QRect(9, 9, 761, 501));
        verticalLayout = new QVBoxLayout(verticalLayoutWidget);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        lowerLabel = new QLabel(verticalLayoutWidget);
        lowerLabel->setObjectName(QStringLiteral("lowerLabel"));

        verticalLayout->addWidget(lowerLabel);

        upperLabel = new QLabel(verticalLayoutWidget);
        upperLabel->setObjectName(QStringLiteral("upperLabel"));

        verticalLayout->addWidget(upperLabel);

        NativePosLabel = new QLabel(verticalLayoutWidget);
        NativePosLabel->setObjectName(QStringLiteral("NativePosLabel"));

        verticalLayout->addWidget(NativePosLabel);

        posLabel = new QLabel(verticalLayoutWidget);
        posLabel->setObjectName(QStringLiteral("posLabel"));

        verticalLayout->addWidget(posLabel);

        horizontalSlider = new QSlider(verticalLayoutWidget);
        horizontalSlider->setObjectName(QStringLiteral("horizontalSlider"));
        horizontalSlider->setStyleSheet(QStringLiteral("color: rgb(255, 85, 127)"));
        horizontalSlider->setOrientation(Qt::Horizontal);

        verticalLayout->addWidget(horizontalSlider);

        TestSliderClass->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(TestSliderClass);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 1103, 26));
        TestSliderClass->setMenuBar(menuBar);
        mainToolBar = new QToolBar(TestSliderClass);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        TestSliderClass->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(TestSliderClass);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        TestSliderClass->setStatusBar(statusBar);

        retranslateUi(TestSliderClass);

        QMetaObject::connectSlotsByName(TestSliderClass);
    } // setupUi

    void retranslateUi(QMainWindow *TestSliderClass)
    {
        TestSliderClass->setWindowTitle(QApplication::translate("TestSliderClass", "TestSlider", 0));
        lowerLabel->setText(QApplication::translate("TestSliderClass", "Lower:", 0));
        upperLabel->setText(QApplication::translate("TestSliderClass", "Upper:", 0));
        NativePosLabel->setText(QApplication::translate("TestSliderClass", "TextLabel", 0));
        posLabel->setText(QApplication::translate("TestSliderClass", "TextLabel", 0));
    } // retranslateUi

};

namespace Ui {
    class TestSliderClass: public Ui_TestSliderClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_TESTSLIDER_H
