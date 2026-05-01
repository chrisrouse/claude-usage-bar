import Foundation
import Sparkle

extension Notification.Name {
    static let openSettingsFromMenu = Notification.Name("openSettingsFromMenu")
}

final class UpdateState: NSObject, ObservableObject, SPUUpdaterDelegate {
    @Published var updateAvailable = false

    func updater(_ updater: SPUUpdater, didFindValidUpdate item: SUAppcastItem) {
        DispatchQueue.main.async { self.updateAvailable = true }
    }

    func updaterDidNotFindUpdate(_ updater: SPUUpdater, error: Error) {
        DispatchQueue.main.async { self.updateAvailable = false }
    }
}
