import QtQuick
import QtQuick.Controls as QQC2
import QtQuick.Layouts
import org.kde.kcmutils as KCM
import org.kde.kirigami as Kirigami

KCM.SimpleKCM {
    id: root
    property string selectedId: ""
    property string searchText: ""
    IslandConfig { id: island }

    function appForId(id) {
        const list = island.applications
        for (let i = 0; i < list.length; ++i)
            if (list[i].id === id) return list[i]
        return null
    }
    readonly property var selectedApp: appForId(selectedId)
    function currentRule() {
        if (!selectedId) return ({})
        const all = island.applicationRules()
        const rule = all[selectedId]
        return rule && typeof rule === "object" ? rule : ({})
    }
    function updateRule(key, value) {
        if (!selectedId) return
        const all = JSON.parse(JSON.stringify(island.applicationRules()))
        const rule = Object.assign({}, all[selectedId] || {})
        if (value === null || value === undefined || value === "inherit")
            delete rule[key]
        else
            rule[key] = value
        if (Object.keys(rule).length) all[selectedId] = rule
        else delete all[selectedId]
        island.set("applicationRules", all)
    }
    function resetRule() {
        if (!selectedId) return
        const all = JSON.parse(JSON.stringify(island.applicationRules()))
        delete all[selectedId]
        island.set("applicationRules", all)
    }
    function selectFirst() {
        if (!selectedId && island.applications.length)
            selectedId = island.applications[0].id
    }
    Connections {
        target: island
        function onApplicationsChanged() { root.selectFirst() }
    }
    Component.onCompleted: selectFirst()

    ColumnLayout {
        anchors.fill: parent
        spacing: Kirigami.Units.smallSpacing
        Kirigami.InlineMessage {
            Layout.fillWidth: true
            visible: island.ready && !island.running
            type: Kirigami.MessageType.Warning
            text: i18n("Dynamic Island is not running. Start it with: systemctl --user start dynamic-island")
        }
        QQC2.Label {
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
            text: i18n("Choose an application to set its notification, sound and display rules. Unchanged settings inherit the global defaults.")
            opacity: 0.75
        }
        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: Kirigami.Units.largeSpacing
            enabled: island.ready
            ColumnLayout {
                Layout.preferredWidth: Kirigami.Units.gridUnit * 13
                Layout.minimumWidth: Kirigami.Units.gridUnit * 11
                Layout.fillHeight: true
                QQC2.TextField {
                    Layout.fillWidth: true
                    placeholderText: i18n("Search applications…")
                    text: root.searchText
                    onTextChanged: root.searchText = text
                    clearButtonEnabled: true
                }
                QQC2.Label {
                    text: i18n("Installed applications: %1").arg(island.applications.length)
                    opacity: 0.65
                    font: Kirigami.Theme.smallFont
                }
                QQC2.Frame {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    padding: 1
                    contentItem: ListView {
                        id: applicationList
                        clip: true
                        model: island.applications.filter(function(app) {
                            return !root.searchText
                                || app.name.toLocaleLowerCase().includes(root.searchText.toLocaleLowerCase())
                                || app.id.toLocaleLowerCase().includes(root.searchText.toLocaleLowerCase())
                        })
                        delegate: QQC2.ItemDelegate {
                            required property var modelData
                            width: ListView.view.width
                            highlighted: modelData.id === root.selectedId
                            onClicked: root.selectedId = modelData.id
                            contentItem: RowLayout {
                                spacing: Kirigami.Units.smallSpacing
                                Kirigami.Icon {
                                    source: modelData.icon || "application-x-executable"
                                    Layout.preferredWidth: Kirigami.Units.iconSizes.medium
                                    Layout.preferredHeight: Kirigami.Units.iconSizes.medium
                                }
                                ColumnLayout {
                                    Layout.fillWidth: true
                                    spacing: 0
                                    QQC2.Label {
                                        Layout.fillWidth: true
                                        text: modelData.name
                                        elide: Text.ElideRight
                                    }
                                    QQC2.Label {
                                        Layout.fillWidth: true
                                        text: modelData.id
                                        opacity: 0.6
                                        elide: Text.ElideMiddle
                                        font: Kirigami.Theme.smallFont
                                    }
                                }
                                QQC2.Label {
                                    visible: !!island.applicationRules()[modelData.id]
                                    text: "•"
                                    color: Kirigami.Theme.highlightColor
                                }
                            }
                        }
                        QQC2.Label {
                            anchors.centerIn: parent
                            visible: applicationList.count === 0
                            text: i18n("No applications found")
                            opacity: 0.65
                        }
                    }
                }
                QQC2.Button {
                    Layout.fillWidth: true
                    text: i18n("Refresh application list")
                    icon.name: "view-refresh"
                    onClicked: island.refreshApplications()
                }
            }
            QQC2.ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumWidth: Kirigami.Units.gridUnit * 16
                contentWidth: availableWidth
                clip: true
                ColumnLayout {
                    width: parent.width
                    spacing: Kirigami.Units.smallSpacing
                    QQC2.Label {
                        Layout.fillWidth: true
                        visible: !root.selectedApp
                        wrapMode: Text.WordWrap
                        text: island.applications.length
                            ? i18n("Select an application from the list.")
                            : i18n("No desktop applications were found. Check that desktop entries are installed.")
                        opacity: 0.7
                    }
                    RowLayout {
                        Layout.fillWidth: true
                        visible: !!root.selectedApp
                        Kirigami.Icon {
                            source: root.selectedApp ? root.selectedApp.icon : "application-x-executable"
                            Layout.preferredWidth: Kirigami.Units.iconSizes.large
                            Layout.preferredHeight: Kirigami.Units.iconSizes.large
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 0
                            QQC2.Label {
                                text: root.selectedApp ? root.selectedApp.name : ""
                                font: Kirigami.Theme.titleFont
                            }
                            QQC2.Label {
                                text: root.selectedId
                                opacity: 0.65
                                font: Kirigami.Theme.smallFont
                            }
                        }
                    }
                    Item { Kirigami.FormData.isSection: true; Kirigami.FormData.label: i18n("Notifications") }
                    QQC2.ComboBox {
                        visible: !!root.selectedApp
                        Layout.fillWidth: true
                        Kirigami.FormData.label: i18n("Notification policy:")
                        textRole: "label"
                        valueRole: "tag"
                        model: [
                            { tag: "inherit", label: i18n("Use global setting") },
                            { tag: "allow", label: i18n("Always allow") },
                            { tag: "mute", label: i18n("Show silently") },
                            { tag: "block", label: i18n("Block notifications") }
                        ]
                        currentIndex: {
                            const value = root.currentRule().notifications || "inherit"
                            for (let i = 0; i < model.length; ++i)
                                if (model[i].tag === value) return i
                            return 0
                        }
                        onActivated: root.updateRule("notifications", model[currentIndex].tag)
                    }
                    QQC2.Label {
                        visible: !!root.selectedApp
                        Layout.fillWidth: true
                        wrapMode: Text.WordWrap
                        opacity: 0.65
                        font: Kirigami.Theme.smallFont
                        text: i18n("Critical notifications always pass through for safety. An explicit Allow can override Do Not Disturb and the legacy blacklist.")
                    }
                    Item { Kirigami.FormData.isSection: true; Kirigami.FormData.label: i18n("Sound") }
                    QQC2.ComboBox {
                        visible: !!root.selectedApp
                        Layout.fillWidth: true
                        Kirigami.FormData.label: i18n("Notification sound:")
                        textRole: "label"
                        valueRole: "tag"
                        model: [
                            { tag: "inherit", label: i18n("Use global setting") },
                            { tag: "on", label: i18n("On") },
                            { tag: "off", label: i18n("Off") }
                        ]
                        currentIndex: {
                            const value = root.currentRule().sound || "inherit"
                            for (let i = 0; i < model.length; ++i)
                                if (model[i].tag === value) return i
                            return 0
                        }
                        onActivated: root.updateRule("sound", model[currentIndex].tag)
                    }
                    Item { Kirigami.FormData.isSection: true; Kirigami.FormData.label: i18n("Display duration") }
                    QQC2.CheckBox {
                        visible: !!root.selectedApp
                        text: i18n("Use a custom duration for this application")
                        checked: Number(root.currentRule().timeout || 0) > 0
                        onToggled: {
                            if (!checked) root.updateRule("timeout", null)
                            else root.updateRule("timeout", 6000)
                        }
                    }
                    QQC2.SpinBox {
                        visible: !!root.selectedApp && Number(root.currentRule().timeout || 0) > 0
                        from: 1000
                        to: 60000
                        stepSize: 500
                        editable: true
                        value: Number(root.currentRule().timeout || 6000)
                        textFromValue: function(value, locale) { return Number(value / 1000).toLocaleString(locale) + " s" }
                        valueFromText: function(text, locale) { return Math.round(Number.fromLocaleString(locale, text.replace(" s", "")) * 1000) }
                        onValueModified: root.updateRule("timeout", value)
                    }
                    Item { Layout.fillHeight: true }
                    QQC2.Button {
                        visible: !!root.selectedApp && !!island.applicationRules()[root.selectedId]
                        Layout.alignment: Qt.AlignRight
                        text: i18n("Reset to global defaults")
                        icon.name: "edit-undo"
                        onClicked: resetDialog.open()
                        QQC2.Dialog {
                            id: resetDialog
                            title: i18n("Reset application settings?")
                            standardButtons: QQC2.Dialog.Yes | QQC2.Dialog.Cancel
                            modal: true
                            onAccepted: root.resetRule()
                            QQC2.Label {
                                text: i18n("All custom rules for this application will be removed.")
                                wrapMode: Text.WordWrap
                            }
                        }
                    }
                }
            }
        }
    }
}
