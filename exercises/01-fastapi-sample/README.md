# Technical Interview Exercises - Python FastAPI sample

これは、[株式会社 ABEJA](https://abejainc.com/ja/) の開発者採用面談で利用するコーディングテストの演習問題のひとつです。

## 制限事項

以下の制限事項を守ってください。

1. Python 3.8 以降を使用してください。
2. ライブラリの追加は行わないでください。

## アプリケーションについて

このアプリケーションは、ユーザ毎の ToDo タスクを管理する API サンプルです。アプリケーションにはユーザ管理機能が含まれています。

タスクとユーザはそれぞれ以下の情報を持ちます。
- タスク: タイトル、説明、担当ユーザ
- ユーザ: メールアドレス、パスワード、有効(`active`)かどうか

コード内では、タスクは `Items` 、ユーザは `User` として表記されます。

API のエンドポイントと提供する機能は以下です。

| Method | Path                     | 機能                             |
|--------|--------------------------|----------------------------------|
| `POST` | `/users/`                | ユーザを作成する。                  |
| `GET`  | `/users/`                | ユーザ一覧を取得する。               |
| `GET`  | `/users/:user_id`        | ユーザ情報を取得する。               |
| `POST` | `/users/:user_id/items/` | あるユーザを担当としてタスクを作成する。|
| `GET`  | `/items/`                | タスク一覧を取得する。               |
| `GET`  | `/health-check`          | ヘルスチェック用エンドポイント        |


### 技術スタック
- 本アプリケーションは [FastAPI](https://fastapi.tiangolo.com/) を利用した Web API です。
- 本アプリケーションは [FastAPI の SQL (Relational) Databases サンプル](https://fastapi.tiangolo.com/tutorial/sql-databases/)をベースにしています。テストは [Testing a Database](https://fastapi.tiangolo.com/advanced/testing-database/) をベースにしています。
- 以下のツールを利用しています。
  - パッケージ管理ツール: [Poetry](https://python-poetry.org/)
  - テストフレームワーク: [pytest](https://docs.pytest.org/)
  - Web アプリケーションフレームワーク: [FastAPI](https://fastapi.tiangolo.com/)
  - データベース: [SQLite3](https://www.sqlite.org/index.html)

## アプリケーションの実行

以下の手順で環境構築を行います。

```bash
$ pip install poetry
$ git clone git@github.com:abeja-inc/system-dev-coding-interview.git
$ cd system-dev-coding-interview/exercises/01-fastapi-sample
$ poetry install
```

以下のコマンドで、アプリケーションをデバッグ実行できます。
```bash
$ make dev
```

以下のコマンドで、テストを実行できます。
```bash
$ make test
```

## 問題 1
APIにユーザ認証機能を実装してください。認証実装後は `X-API-TOKEN` をリクエストヘッダに入れる事でユーザ認証を行う事とします。ただし、ユーザ作成エンドポイント (`POST /users`) は無認証で受け付ける事とします。`X-API-TOKEN` はユーザ作成時に発行し、レスポンスに含めます。
また、変更に伴うテストケースの修正・追加を行ってください。

## 問題 2
自分が所有している `item` を取得するエンドポイントを追加してください。エンドポイントは `GET /me/items` とします。
また、必要なテストケースの追加を行ってください。

## 問題 3
ユーザの削除を行うエンドポイントを追加してください。ユーザの削除は、`is_active` を `False` にする事で行います。
その際、削除対象のユーザが所有する `item` は、有効なユーザかつ `id` が最も小さなユーザの所有権を移す事とします。
また、必要なテストケースの追加を行ってください。

