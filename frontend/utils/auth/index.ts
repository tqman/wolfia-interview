import {useCurrentUser} from "@/api/Auth";

export const useIsLoggedIn = (): boolean => useCurrentUser().data !== undefined;
