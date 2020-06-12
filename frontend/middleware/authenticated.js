export default function ({ $auth, redirect, route }) {
  if (!$auth.loggedIn && route.path !== '/login') {
    return redirect('/login')
  }
}
