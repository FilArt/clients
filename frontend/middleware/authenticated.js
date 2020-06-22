export default function ({ $auth, redirect, route }) {
  if (!$auth.loggedIn && route.name !== 'login') {
    return redirect('/login')
  }
}
