# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Released]

### 1.2 - 2019-06-11
#### Added
- profile images for user list
- bugfix for authenticated user to change its password

### 1.1 - 2019-06-03
#### Added
- electric point list filter by point name
- electric point display name changed
- project list filter by progress status
- project detail left side bar item list updated to show the projected point and suggested point
- prokect list filter by region and equipment type

### 1.0 - 2019-05-27
#### Added
- dashborad index with progress status cards

## [Unreleased]

### 0.0 - 2019-05-10
#### Added
- project management app: {
    list projects
    update project
    update project trace number
    relare pendency to project
    relate new location to project electric point
    relate step to project
    delete project
    update progress status
}
- electric point management app: {
    create point
    delete point
    list points
    relate project to point
    relate coverage study to point
    relate feeder study to point
    relate supply delivery to point
}
- user management app: {
    create user
    update user
    delete user (hard delete)
    read user (without action history)
    list users
    user profile management (hardcoded)
    update password
    toggle admin status
    toggle activation status
    authentication login
    authentication logout
}
- project created