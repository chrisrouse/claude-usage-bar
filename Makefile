APP_NAME   = Claude Usage Bar
VERSION    = 0.1.0
DMG_NAME   = Claude-Usage-Bar-$(VERSION).dmg
BUILD_DIR  = dist

.PHONY: all icon app dmg clean

all: dmg

icon:
	python3 scripts/make_icon.py

## Build the self-contained .app bundle via PyInstaller
app: icon
	pyinstaller --clean --noconfirm claude_usage_bar.spec
	@echo "\n✅  App bundle: $(BUILD_DIR)/$(APP_NAME).app"

## Wrap the .app in a distributable .dmg with an Applications symlink
dmg: app
	@rm -f "$(BUILD_DIR)/$(DMG_NAME)"
	@mkdir -p "$(BUILD_DIR)/dmg-staging"
	@cp -r "$(BUILD_DIR)/$(APP_NAME).app" "$(BUILD_DIR)/dmg-staging/"
	@ln -sf /Applications "$(BUILD_DIR)/dmg-staging/Applications"
	hdiutil create \
		-volname "$(APP_NAME)" \
		-srcfolder "$(BUILD_DIR)/dmg-staging" \
		-ov \
		-format UDZO \
		"$(BUILD_DIR)/$(DMG_NAME)"
	@rm -rf "$(BUILD_DIR)/dmg-staging"
	@echo "\n✅  DMG ready: $(BUILD_DIR)/$(DMG_NAME)"

clean:
	rm -rf build dist
