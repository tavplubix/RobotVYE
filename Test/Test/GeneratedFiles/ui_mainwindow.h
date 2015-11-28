/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.5.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QWidget *gridLayoutWidget;
    QGridLayout *gridLayout;
    QCheckBox *showResultCheckBox;
    QCheckBox *showOriginalCheckBox;
    QHBoxLayout *horizontalLayout;
    QLabel *beforeLabel;
    QFrame *line_2;
    QLabel *maskLabel;
    QFrame *line_3;
    QLabel *afterLabel;
    QFrame *line;
    QCheckBox *showMaskCheckBox;
    QFormLayout *formLayout_2;
    QFormLayout *formLayout_3;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(1108, 803);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        gridLayoutWidget = new QWidget(centralWidget);
        gridLayoutWidget->setObjectName(QStringLiteral("gridLayoutWidget"));
        gridLayoutWidget->setGeometry(QRect(10, 10, 1041, 461));
        gridLayout = new QGridLayout(gridLayoutWidget);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QStringLiteral("gridLayout"));
        gridLayout->setContentsMargins(0, 0, 0, 0);
        showResultCheckBox = new QCheckBox(gridLayoutWidget);
        showResultCheckBox->setObjectName(QStringLiteral("showResultCheckBox"));
        showResultCheckBox->setChecked(true);

        gridLayout->addWidget(showResultCheckBox, 2, 3, 1, 1);

        showOriginalCheckBox = new QCheckBox(gridLayoutWidget);
        showOriginalCheckBox->setObjectName(QStringLiteral("showOriginalCheckBox"));
        showOriginalCheckBox->setChecked(true);

        gridLayout->addWidget(showOriginalCheckBox, 0, 3, 1, 1);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        beforeLabel = new QLabel(gridLayoutWidget);
        beforeLabel->setObjectName(QStringLiteral("beforeLabel"));

        horizontalLayout->addWidget(beforeLabel);

        line_2 = new QFrame(gridLayoutWidget);
        line_2->setObjectName(QStringLiteral("line_2"));
        line_2->setFrameShadow(QFrame::Raised);
        line_2->setLineWidth(5);
        line_2->setFrameShape(QFrame::VLine);

        horizontalLayout->addWidget(line_2);

        maskLabel = new QLabel(gridLayoutWidget);
        maskLabel->setObjectName(QStringLiteral("maskLabel"));

        horizontalLayout->addWidget(maskLabel);

        line_3 = new QFrame(gridLayoutWidget);
        line_3->setObjectName(QStringLiteral("line_3"));
        line_3->setFrameShadow(QFrame::Raised);
        line_3->setLineWidth(5);
        line_3->setFrameShape(QFrame::VLine);

        horizontalLayout->addWidget(line_3);

        afterLabel = new QLabel(gridLayoutWidget);
        afterLabel->setObjectName(QStringLiteral("afterLabel"));

        horizontalLayout->addWidget(afterLabel);


        gridLayout->addLayout(horizontalLayout, 7, 1, 1, 3);

        line = new QFrame(gridLayoutWidget);
        line->setObjectName(QStringLiteral("line"));
        line->setFrameShadow(QFrame::Raised);
        line->setLineWidth(5);
        line->setFrameShape(QFrame::HLine);

        gridLayout->addWidget(line, 6, 1, 1, 3);

        showMaskCheckBox = new QCheckBox(gridLayoutWidget);
        showMaskCheckBox->setObjectName(QStringLiteral("showMaskCheckBox"));
        showMaskCheckBox->setChecked(true);

        gridLayout->addWidget(showMaskCheckBox, 1, 3, 1, 1);

        formLayout_2 = new QFormLayout();
        formLayout_2->setSpacing(6);
        formLayout_2->setObjectName(QStringLiteral("formLayout_2"));
        formLayout_2->setHorizontalSpacing(7);
        formLayout_2->setVerticalSpacing(7);
        formLayout_2->setContentsMargins(0, 0, -1, -1);

        gridLayout->addLayout(formLayout_2, 0, 1, 4, 1);

        formLayout_3 = new QFormLayout();
        formLayout_3->setSpacing(6);
        formLayout_3->setObjectName(QStringLiteral("formLayout_3"));

        gridLayout->addLayout(formLayout_3, 0, 2, 4, 1);

        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 1108, 26));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", 0));
        showResultCheckBox->setText(QApplication::translate("MainWindow", "Show result", 0));
        showOriginalCheckBox->setText(QApplication::translate("MainWindow", "Show original", 0));
        beforeLabel->setText(QApplication::translate("MainWindow", "Before", 0));
        maskLabel->setText(QApplication::translate("MainWindow", "Mask", 0));
        afterLabel->setText(QApplication::translate("MainWindow", "After", 0));
        showMaskCheckBox->setText(QApplication::translate("MainWindow", "Show mask", 0));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
