# #9 - Demanage

Boarding-style project dev management system/website/web app/web API/web service/tool/platform. In contract to general project management systems this project only focuses on the kanban style of management (basically boards).

Goals of this project:

- learn production-ready (real-world) project setup

- finalize technologies coverage (task queue) 

- learn hybric webapp architecture

Similar applications:

- **Trello**

- Taiga.io

## Description/requirements

## Roadmap

- Models

- MVTs

- Permissions

- APIs

- Celery

- Integrations

### Todo

- [x] Project setup

- [x] Organization model + admin interface

- [ ] Organization MVT user interface

- [ ] Organization representative permission group

- [ ] Organization member model

- [ ] Organization member inviting

- [ ] Organization member permission group

- [ ] Organization administrator permission group

- [ ] Board model/admin + API

- [ ] Task API

- [ ] Notifications

### Design

The idea of this app is to help teams work together on a project more productively. By managing tasks and progress in the cloud (synchronization). It also allows access from any device connected to the web.

User flow:

1. User registers a new account (verifies email address) and loges-in. User profile might have avatar, username, current life status, company name.

2. User creates a team (project) and becomes it's *creator/owner*. User sets up initial boards, lists and tasks for the teammates. User chooses to create public or private team.

3. Not invited users can read board as visitors/guests by shared link.

4. Creator invites other users to join team via unique generated *invite link*. Invited users get *member* role and are able to do basic project manipulations.

5. Creator sets administrators from members and can transfer ownership to other users.

Work flow:

1. Teammates design project structure (boards and lists). Design roadmap, features, backlog. Idea, backlog, to-do, in progress, review, done list as kinda easy-to-change task statuses.

2. Team creates tasks (cards, features), add design, description, split into subtasks, set due date. Users can tag tasks based on importance, technology, difficulty

3. Manager or teammates add assignees to the task and move to in-progress list. Start working on the task, may write comments while doing.

### Permissions

Short website permission description:

- Admins can add users to organization representative group.

- Organization representative group users can create/delete single organization from MVT interface.

- Owner can update team and set member permissions from MVT.

- Team administrators can create/delete boards and invite members from API/SPA.

- Members can update boards and create/update/delete lists and tasks from SPA (API).

### Organization

Organization model:

- name field - unicode char field (required).

- slug field - created from unicode name, slug also support unicode  (required in the model and admin, not shown in MVT) (prepolulated in the admin and set from name in the form).

- location field - contains real world country (default=US).

- verified field - editable from admin interface, disabled (read-only) from MVT interface (default=False).

- website_url field - contains organization website or blog URL (optional).

- public field - controls whether the organization is visible (viewable) by non-members (default=True).

Organization permission asserted **test cases**:

- Superuser has permission to create organizations, view/delete/update any organization.

- Organization representative has permission to create organization instance.

- Users not in org repr. group don't have permission to create or delete any organizations.
  Superuser and org representative have permission to add user to the organization administration group, organization administrators and members don't.

- Organization administrator has permission to update organization.

- Org. repr. can not create more than 1 organization instance.

- Org. repr. has permission to view, update and delete their organization instance.

- Other org representatives don't have permission to delete or update other org instances.

- Org members have permission to view their public/private organization.

- Everyone can view public organization.

- Superuser has permission to update organization verified status.

- Organization representative, administrator and member have permission to view verified status, and aren't able to update it (read-only field).

- Org representative, org administrators or org members don't have permission to update organization verified status.

Organization representative group should be available without creating it via admin interface (created at the migration stage).

Permissions and groups work like a user tagging to any actions they are allowed. There are available following permission system options:

1. model-level (website-level)

2. field-level

3. instance-level (user-level)

### Project

Initial project was generated using Cookicutter Django template and provide following features:

- reStructuredTest readme, licence, etc.

- authentication model, templates, view, etc.

- redis

- celery, django celery beat (backend)

- flower for celery worker monitoring

- django packages: allauth, crispy forms (bootstrap)

- local/production separation (docker compose, settings, requirements)

- testing, code quality, debugging, documentation Python packages

- sphinx docs

- aws, mailgun, sentry, github

- postgresql

### Hybrid Architecture (full stack rendering)

The project will have the following parts:

- MVT part: server-side rendered pages (not interactive dynamic pages like about, register, login, information, teams creation...)

- API part: RESTful web API routes for making interactive SPA part (like CRUD API for boards, task and other dynamic elements)

- SPA part: dynamic, interactive, client-side rendered AJAX single page (utilizes API to be fast without page reloading) (like boards/lists/tasks on-the-fly from pop-up) + illustrative routes for more structured  (react-router)

### About

What is this project about?

- organization

- team

- planning

- management (time/resources)

- collaboration

- productivity

- kanban

### Features

> More features is only better for the project.

*Potential* project feature list.

Traditions:

- RESTful web API for single-page application

- Mindful test-driven development

- Mindful code coverage

- Improve test quality over quantity

Innovations:

- tasks/assignments

- tagging

- important dates

- events

- internationalization (MVT, API, SPA)

- timeline, deadlines

- real-world usage

- team collaboration (assignees)

- e-mail confirmation (Twilio/SendGrid)

- teams/workspaces/boards/lists/cards

- generate unique (random) invite links/board URIs

- print to PDF or Google Docs

- 3-rd party service integration (library/SDK)

- user system (admins, members, visitors)

- CRUD object-level permissions

- notifications (email, SMS, 3-rd party service)

- import dataset or 3-rd party API

- integrated chat (embedded URLs/views)

- geolocation/photo/video/media cards

- card media attachments

### Integration

Integrations with other business services:

- Slack

- Jira

- Teams

- Dropbox

## Technology

*Potential* (nice to have) list of technologies involved in this project. Not implemented features move to the next projects.

Technologies:

- core: RESTful web API

- additional: asynchronous/background API features

Traditions:

- Django REST Framework
- API usability features
- JWT authentication
- Redis caching
- Docker containerization

Innovations:

- cookiecutter
- custom admin theme/interface
- task queue (Celery)
- message broker (RabbitMQ)
- task worker
- PDF generation
- 3-rd party APIs
- 3-rd party Python packages
- 3-rd party Django packages
- error reporting
- integrated chat
- custom Swagger UI theme
- django command extensions
- push notification to mobile devices
- send emails/SMS service

## Web services

List of potential web services that will be used in this projects:

- Mailgun (email)

- GitHub Actions (CI/CD)

- AWS (cloud)

- Sentry (monitoring)